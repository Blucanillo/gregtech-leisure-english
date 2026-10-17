package local.translationaudit;

import com.google.gson.GsonBuilder;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.network.chat.Component;
import net.minecraftforge.client.event.ScreenEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.event.TickEvent;
import net.minecraft.world.level.LevelSettings;
import net.minecraft.world.level.GameType;
import net.minecraft.world.Difficulty;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.WorldDataConfiguration;
import net.minecraft.world.level.levelgen.WorldOptions;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.Pattern;

/** Disposable integration-test mod. Never distribute inside the translation. */
@Mod("translation_runtime_audit")
public class TranslationRuntimeAudit {
  private static final Pattern CHINESE=Pattern.compile("[\\u3400-\\u9fff]");
  private static final Pattern RAW=Pattern.compile("(?:item|block|material)\\.[a-z0-9_]+\\.[a-z0-9_./]+|gtl1450\\.[a-z0-9_.]+|gtmthings\\.machine\\.[a-z0-9_.]+");
  private final List<Map<String,Object>> names=new ArrayList<>(),tooltips=new ArrayList<>(),errors=new ArrayList<>();
  private List<Item> items;
  private int next,frames,capture;
  private boolean finished;
  private boolean worldRequested,worldScanned;
  private int worldNext,worldFrames;
  private final List<Map<String,Object>> worldErrors=new ArrayList<>(),worldTooltips=new ArrayList<>();
  private int guideCapture,guideFrames;
  private final String[] guideScreens={"index.md","example-setups/bucket-emptier.md","example-setups/bucket-filler.md","example-setups/recursive-crafting-setup.md","items-blocks-machines/fluix_researcher.md","example-setups/main-network.md","items-blocks-machines/formation_plane.md"};
  public TranslationRuntimeAudit(){MinecraftForge.EVENT_BUS.register(this);}
  private static Map<String,Object> row(Object... fields){
    Map<String,Object> result=new LinkedHashMap<>();
    for(int i=0;i<fields.length;i+=2)result.put((String)fields[i],fields[i+1]);
    return result;
  }
  private static boolean bad(String text){return CHINESE.matcher(text).find()||RAW.matcher(text).find();}
  private void write(Minecraft mc)throws Exception {
    Map<String,Object> result=row("phase","full-live-registry-and-tooltips","language",mc.m_91102_().m_264236_(),"names",names,"tooltips",tooltips,"errors",errors,"screenshots_completed",capture);
    Files.writeString(mc.f_91069_.toPath().resolve("translation-runtime-full-result.json"),new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(result),StandardCharsets.UTF_8);
  }
  @SubscribeEvent
  public void render(ScreenEvent.Render.Post event) {
    String screen=event.getScreen().getClass().getName();
    if(event.getScreen() instanceof guideme.internal.screen.GuideScreen guideScreen && worldScanned){
      if(guideCapture>=guideScreens.length || ++guideFrames<20)return;
      Minecraft mc=Minecraft.m_91087_();
      event.getGuiGraphics().m_280262_();
      Screenshot.m_92295_(mc.f_91069_,"translation-guide-"+guideCapture+".png",mc.m_91385_(),message->System.out.println("TRANSLATION_AUDIT_GUIDE_CAPTURE: "+message.getString()));
      guideCapture++;guideFrames=0;
      if(guideCapture<guideScreens.length)guideScreen.navigateTo(new ResourceLocation("ae2",guideScreens[guideCapture]));
      else {System.out.println("TRANSLATION_AUDIT_GUIDE_RENDER_DONE");mc.m_91152_(null);mc.m_91395_();}
      return;
    }
    if(!(screen.contains("TitleScreen")||screen.contains("ExtendedMenuScreen")))return;
    Minecraft mc=Minecraft.m_91087_();
    try {
      if(items==null){
        if(++frames<30)return;
        items=new ArrayList<>();BuiltInRegistries.f_257033_.forEach(items::add);
        System.out.println("TRANSLATION_AUDIT_NATIVE_START: "+items.size()+" registered items");
      }
      if(!finished){
        int end=Math.min(next+256,items.size());
        for(;next<end;next++){
          Item item=items.get(next);String id=BuiltInRegistries.f_257033_.m_7981_(item).toString();
          ItemStack stack=new ItemStack(item);
          try{
            String key=stack.m_41778_(),name=stack.m_41786_().getString();
            names.add(row("id",id,"key",key,"name",name));
            if(name.isBlank()||bad(name))errors.add(row("id",id,"kind","untranslated-name","text",name));
            List<String> lines=stack.m_41651_(null,new TooltipFlag.Default(false,false)).stream().map(Component::getString).toList();
            tooltips.add(row("id",id,"lines",lines));
            for(String line:lines)if(bad(line))errors.add(row("id",id,"kind","bad-tooltip","text",line));
          }catch(Throwable error){errors.add(row("id",id,"kind","item-probe-error","text",error.toString()));}
        }
        if(next>=items.size()){
          finished=true;frames=0;write(mc);
          System.out.println("TRANSLATION_AUDIT_NATIVE_DONE: names="+names.size()+" tooltips="+tooltips.size()+" errors="+errors.size());
        }
        return;
      }
      if(capture<6){
        if(++frames<20)return;
        String[] ids={"kubejs:supracausal_mainframe","kubejs:luv_universal_circuit","gtmthings:me_export_buffer","gtmthings:lv_digital_miner","gtceu:spacetime_ingot","gtceu:chemical_energy_devourer"};
        ItemStack stack=new ItemStack(BuiltInRegistries.f_257033_.m_7745_(new ResourceLocation(ids[capture])));
        GuiGraphics graphics=event.getGuiGraphics();
        graphics.m_280509_(0,0,graphics.m_280182_(),graphics.m_280206_(),0xff171717);
        graphics.m_280480_(stack,12,12);
        graphics.m_280153_(mc.f_91062_,stack,35,35);
        graphics.m_280262_();
        String filename="translation-native-"+capture+".png";
        Screenshot.m_92295_(mc.f_91069_,filename,mc.m_91385_(),message->System.out.println("TRANSLATION_AUDIT_NATIVE_CAPTURE: "+message.getString()));
        capture++;frames=0;write(mc);
      } else if(!worldRequested){
        worldRequested=true;
        String world="Translation-Audit-"+System.currentTimeMillis();
        System.out.println("TRANSLATION_AUDIT_CREATE_FRESH_WORLD: "+world);
        mc.m_231466_().m_233157_(world,new LevelSettings(world,GameType.CREATIVE,false,Difficulty.PEACEFUL,true,new GameRules(),WorldDataConfiguration.f_244649_),new WorldOptions(14501452L,false,false),WorldPresets::m_246552_);
      }
    }catch(Throwable error){
      finished=true;capture=3;errors.add(row("kind","native-harness-error","text",error.toString()));
      error.printStackTrace();try{write(mc);}catch(Exception ignored){}
    }
  }
  @SubscribeEvent
  public void tick(TickEvent.ClientTickEvent event){
    if(event.phase!=TickEvent.Phase.END || !worldRequested || worldScanned)return;
    Minecraft mc=Minecraft.m_91087_();
    if(mc.f_91073_==null || mc.f_91074_==null || ++worldFrames<60)return;
    try {
      int end=Math.min(worldNext+128,items.size());
      for(;worldNext<end;worldNext++){
        Item item=items.get(worldNext);String id=BuiltInRegistries.f_257033_.m_7981_(item).toString();
        ItemStack stack=new ItemStack(item);
        for(boolean advanced:new boolean[]{false,true}){
          try{
            List<String> lines=stack.m_41651_(mc.f_91074_,new TooltipFlag.Default(advanced,false)).stream().map(Component::getString).toList();
            worldTooltips.add(row("id",id,"advanced",advanced,"lines",lines));
            for(String line:lines)if(bad(line))worldErrors.add(row("id",id,"kind","bad-world-tooltip","advanced",advanced,"text",line));
          }catch(Throwable error){worldErrors.add(row("id",id,"kind","world-probe-error","advanced",advanced,"text",error.toString()));}
        }
      }
      if(worldNext>=items.size()){
        worldScanned=true;
        Map<String,Object> result=row("phase","fresh-world-normal-and-advanced-tooltips","language",mc.m_91102_().m_264236_(),"registered_items",items.size(),"tooltips",worldTooltips,"errors",worldErrors,"original_worlds_copied",false);
        Files.writeString(mc.f_91069_.toPath().resolve("translation-runtime-world-result.json"),new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(result),StandardCharsets.UTF_8);
        System.out.println("TRANSLATION_AUDIT_WORLD_DONE: tooltips="+worldTooltips.size()+" errors="+worldErrors.size());
        auditGuides(mc);
      }
    }catch(Throwable error){worldScanned=true;error.printStackTrace();}
  }
  private void auditGuides(Minecraft mc)throws Exception {
    List<Map<String,Object>> pages=new ArrayList<>(),issues=new ArrayList<>();
    guideme.Guide guide=guideme.Guides.getAll().stream().filter(g->g.getDefaultNamespace().equals("ae2") && g.getContentRootFolder().equals("ae2guide")).findFirst().orElseThrow();
    Path root=mc.f_91069_.toPath().resolve("kubejs/assets/ae2/ae2guide");
    try(var paths=Files.walk(root)){
      for(Path path:paths.filter(p->p.toString().endsWith(".md")).sorted().toList()){
        String relative=root.relativize(path).toString().replace('\\','/');
        try{
          guideme.GuidePage page=guide.getPage(new ResourceLocation("ae2",relative));
          if(page==null)throw new IllegalStateException("No compiled guide page");
          String text=page.document().getTextContent();
          pages.add(row("page",relative,"source_pack",page.sourcePack(),"text",text));
          if(CHINESE.matcher(text).find() || text.contains("Couldn't find recipe") || text.contains("Couldn't load") || text.contains("Unknown item"))issues.add(row("page",relative,"kind","invalid-rendered-guide-text","text",text));
        }catch(Throwable error){issues.add(row("page",relative,"kind","guide-compile-error","text",error.toString()));}
      }
    }
    Files.writeString(mc.f_91069_.toPath().resolve("translation-runtime-guide-result.json"),new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(row("guide",guide.getId().toString(),"pages",pages,"errors",issues)),StandardCharsets.UTF_8);
    System.out.println("TRANSLATION_AUDIT_GUIDE_DONE: pages="+pages.size()+" errors="+issues.size());
    mc.m_91152_(guideme.internal.screen.GuideScreen.openNew(guide,guideme.PageAnchor.page(new ResourceLocation("ae2",guideScreens[0]))));
  }
}
