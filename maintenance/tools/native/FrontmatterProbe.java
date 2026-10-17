import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import guideme.compiler.Frontmatter;
import net.minecraft.resources.ResourceLocation;

public class FrontmatterProbe {
  public static void main(String[] args) throws Exception {
    int count=0, failed=0;
    Path root=Path.of(args[0]);
    try(var paths=Files.walk(root)) {
      for(var path:paths.filter(p->p.toString().endsWith(".md")).toList()) {
        try {
          String text=Files.readString(path,StandardCharsets.UTF_8).replaceAll("\\r\\n?","\n");
          String yaml=text.split("---",3)[1];
          var id=new ResourceLocation("ae2",root.relativize(path).toString().replace('\\','/'));
          var parsed=Frontmatter.parse(id,yaml);
          if(parsed.navigationEntry()==null)throw new IllegalStateException("Missing navigation entry");
          count++;
        } catch(Throwable e) {
          failed++;
          System.out.println("FAIL "+path+" "+e);
          e.printStackTrace(System.out);
        }
      }
    }
    System.out.println("FRONTMATTER_PARSED="+count+" FAILED="+failed);
    if(failed>0)System.exit(1);
  }
}
