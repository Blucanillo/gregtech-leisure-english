import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.util.zip.*;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.FormattedText;
import net.minecraft.util.FormattedCharSequence;
import net.minecraftforge.common.ForgeI18n;
import com.google.gson.JsonParser;

/** Exercises Minecraft's actual language loader and component substitution. */
public class LanguageProbe {
  static class Dictionary extends Language {
    final Map<String,String> values;
    Dictionary(Map<String,String> values){this.values=values;}
    public String m_118919_(String key,String fallback){return values.getOrDefault(key,fallback);}
    public boolean m_6722_(String key){return values.containsKey(key);}
    public boolean m_6627_(){return false;}
    public FormattedCharSequence m_5536_(FormattedText text){return FormattedCharSequence.f_13691_;}
  }
  public static void main(String[] args)throws Exception {
    Map<String,String> values=new LinkedHashMap<>();
    try(var zip=new ZipFile(args[0])) {
      for(var entry:zip.stream().toList()) {
        if(entry.getName().endsWith("/lang/en_us.json")) {
          try(var stream=zip.getInputStream(entry)){Language.m_128108_(stream,values::put);}
        }
      }
    }
    Language.m_128114_(new Dictionary(values));
    Pattern parameters=Pattern.compile("%(?:(\\d+)\\$)?([A-Za-z%])");
    int checked=0,formatted=0,failed=0,forgeTemplates=0;
    com.google.gson.JsonObject nativeForge;
    try(var nativeZip=new ZipFile(args[1]);var input=nativeZip.getInputStream(nativeZip.getEntry("assets/forge/lang/en_us.json"))) {
      nativeForge=JsonParser.parseReader(new java.io.InputStreamReader(input,StandardCharsets.UTF_8)).getAsJsonObject();
    }
    for(var entry:values.entrySet()) {
      if(entry.getKey().startsWith("fml.") && entry.getValue().matches("(?s).*\\{\\d+,[^}]*}.*")) {
        // Forge's message templates use ExtendedMessageFormat, not vanilla
        // Component arguments. These entries must retain the native template.
        if(!nativeForge.has(entry.getKey()) || !nativeForge.get(entry.getKey()).getAsString().equals(entry.getValue()))throw new IllegalStateException("Changed native Forge template: "+entry.getKey()+" NATIVE="+nativeForge.get(entry.getKey())+" LOADED="+entry.getValue());
        forgeTemplates++;continue;
      }
      var matcher=parameters.matcher(entry.getValue());
      StringBuilder expected=new StringBuilder();
      int ordinal=0,max=0;
      while(matcher.find()) {
        String replacement;
        if(matcher.group(2).equals("%"))replacement="%";
        else {
          if(!matcher.group(2).equals("s"))throw new IllegalStateException("Unnormalized format: "+entry);
          int index=matcher.group(1)==null?++ordinal:Integer.parseInt(matcher.group(1));
          max=Math.max(max,index);replacement="AUDIT_ARG_"+index;
        }
        matcher.appendReplacement(expected,Matcher.quoteReplacement(replacement));
      }
      matcher.appendTail(expected);
      Object[] arguments=new Object[max];
      for(int i=0;i<max;i++)arguments[i]="AUDIT_ARG_"+(i+1);
      String actual=Component.m_237110_(entry.getKey(),arguments).getString();
      if(!actual.equals(expected.toString())) {
        failed++;System.out.println("FAIL "+entry.getKey()+" expected="+expected+" actual="+actual);
      }
      checked++;if(max>0)formatted++;
    }
    ForgeI18n.loadLanguageData(values);
    for(int amount:new int[]{0,1,5}) {
      String actual=ForgeI18n.parseMessage("fml.menu.loadingmods",amount);
      String expected=amount==0?"No mods loaded":amount==1?"1 mod loaded":"5 mods loaded";
      if(!actual.equals(expected))throw new IllegalStateException("Forge plural format: "+actual);
    }
    System.out.println("COMPONENT_KEYS="+checked+" PARAMETERIZED="+formatted+" NATIVE_FORGE_TEMPLATES="+forgeTemplates+" FORGE_PLURAL_CASES=3 FAILED="+failed);
    if(failed>0)System.exit(1);
  }
}
