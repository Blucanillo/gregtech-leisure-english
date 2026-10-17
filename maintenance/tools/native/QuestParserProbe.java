import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import dev.ftb.mods.ftblibrary.snbt.SNBT;

/** Parses the actual distributed files with the matching installed FTB parser. */
public class QuestParserProbe {
  public static void main(String[] args)throws Exception {
    Path root=Path.of(args[0]),source=Path.of(args[1]);
    int parsed=0,empty=0,failed=0;
    try(var paths=Files.walk(root)) {
      for(var path:paths.filter(p->p.toString().endsWith(".snbt")).toList()) {
        try {
          String text=Files.readString(path,StandardCharsets.UTF_8);
          if(text.isBlank()) {
            if(!Files.readString(source.resolve(root.relativize(path)),StandardCharsets.UTF_8).isBlank())throw new IllegalStateException("A nonempty source was erased");
            empty++;continue;
          }
          if(SNBT.readLines(Files.readAllLines(path,StandardCharsets.UTF_8))==null)throw new IllegalStateException("Null parse result");
          parsed++;
        } catch(Throwable e) {
          failed++;System.out.println("FAIL "+path+" "+e);e.printStackTrace(System.out);
        }
      }
    }
    System.out.println("QUEST_FILES_PARSED="+parsed+" UNCHANGED_EMPTY_FILES="+empty+" FAILED="+failed);
    if(failed>0)System.exit(1);
  }
}
