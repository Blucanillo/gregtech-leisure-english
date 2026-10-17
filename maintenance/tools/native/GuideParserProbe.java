import guideme.libs.mdast.MdAst;
import guideme.libs.mdast.MdastOptions;
import guideme.libs.mdx.MdxSyntax;
import guideme.libs.micromark.extensions.YamlFrontmatterSyntax;
import guideme.libs.micromark.extensions.gfm.GfmTableSyntax;
import guideme.libs.micromark.extensions.gfmstrikethrough.GfmStrikethroughSyntax;
import guideme.libs.mdast.mdx.MdxMdastExtension;
import guideme.libs.mdast.YamlFrontmatterExtension;
import guideme.libs.mdast.gfm.GfmTableMdastExtension;
import guideme.libs.mdast.gfmstrikethrough.GfmStrikethroughMdastExtension;
import com.google.gson.stream.JsonWriter;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;

/** Uses the actual installed GuideME parser and PageCompiler's exact extensions. */
public class GuideParserProbe {
  public static void main(String[] args) throws Exception {
    var options = new MdastOptions()
        .withSyntaxExtension(MdxSyntax.INSTANCE)
        .withSyntaxExtension(YamlFrontmatterSyntax.INSTANCE)
        .withSyntaxExtension(GfmTableSyntax.INSTANCE)
        .withSyntaxExtension(GfmStrikethroughSyntax.INSTANCE)
        .withMdastExtension(MdxMdastExtension.INSTANCE)
        .withMdastExtension(YamlFrontmatterExtension.INSTANCE)
        .withMdastExtension(GfmTableMdastExtension.INSTANCE)
        .withMdastExtension(GfmStrikethroughMdastExtension.INSTANCE);
    int count=0, failed=0;
    Path root=Path.of(args[0]), out=Path.of(args[1]);
    try (var paths=Files.walk(root)) {
      for (var path:paths.filter(p->p.toString().endsWith(".md")).toList()) {
        String text=Files.readString(path,StandardCharsets.UTF_8).replaceAll("\\r\\n?","\n");
        try {
          var ast=MdAst.fromMarkdown(text,options);
          var destination=out.resolve(root.relativize(path)+".json");
          Files.createDirectories(destination.getParent());
          try(var writer=new JsonWriter(Files.newBufferedWriter(destination,StandardCharsets.UTF_8))) {
            ast.toJson(writer);
          }
          count++;
        } catch (Throwable e) {
          failed++;
          System.out.println("FAIL "+path+" "+e);
          e.printStackTrace(System.out);
        }
      }
    }
    System.out.println("PARSED="+count+" FAILED="+failed);
    if(failed>0)System.exit(1);
  }
}
