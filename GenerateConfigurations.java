import org.nlogo.headless.HeadlessWorkspace;

import static java.lang.System.out;
import static java.lang.System.err;
import static java.lang.String.format;

public class GenerateConfigurations {
  // number of steps
  static int steps = 250;

  // global parameters

  public static void main(String[] argv) {

    int world_size = Integer.parseInt(argv[0]);
    int init_life = Integer.parseInt(argv[1]);
    boolean rand = Boolean.parseBoolean(argv[2]);
    boolean sync = Boolean.parseBoolean(argv[3]);
    
    int deterministic_period = Integer.parseInt(argv[4]);
    double rule_switch_prob = Double.parseDouble(argv[5]);
    int second_threshold =  Integer.parseInt(argv[6]);

    HeadlessWorkspace world = HeadlessWorkspace.newInstance();
    try {
      world.open("life-rule-switching.nlogo");

      //for (int st = second_threshold; st<=9; st++) {
      //  for (double p = 0.0; p<1.0; p+=0.1) {
          runWorld(world, world_size, init_life, rand, sync, 
              deterministic_period, rule_switch_prob, second_threshold);
      //  }
      //}

      world.dispose();
    } catch (Exception ex) {
      ex.printStackTrace();
    }

  }

  private static void runWorld(
      HeadlessWorkspace world, 
      int world_size, int init_life, boolean rand, boolean sync, 
      int deterministic_period, double rule_switch_prob, int second_threshold) {

    err.println("[INFO] restarting simulation!");

    // name is build from the parsed values
    String world_name = new String();

    try {
      // load the model

      // model specific setup
      world.command(format("set world-size %d", world_size));
      out.println(format("set world-size %d", world_size));

      world.command(format("set init-life %d", init_life));
      out.println(format("set init-life %d", init_life));

      world_name += format("_size%d", world_size); 
      world_name += format("_init%d", init_life); 

      if (sync) {
        world.command("set synchronous true");
        world_name += "_sync"; 
      } else { 
        world.command("set synchronous false");
        world_name += "_async"; 
      }

      if (rand) {
        world_name += "_rand";
        world_name += format("_p%3.2f", rule_switch_prob);
        world.command("set deterministic false");
        err.println("set deterministic false");

        world.command(format("set rule-switch-prob %3.2f", rule_switch_prob)); 
        err.println(format("set rule-switch-prob %3.2f", rule_switch_prob)); 

      } else { 
        world.command("set deterministic true");
        err.println("set deterministic true");

        world.command(format("set deterministic-period %d", deterministic_period));
        err.println(format("set deterministic-period %d", deterministic_period));

        world_name += "_detr"; 
        world_name += format("_dp%d", deterministic_period); 
      }

      world_name += format("_st%d", second_threshold);
      world.command(format("set second-threshold %d", second_threshold));
      err.println(format("set second-threshold %d", second_threshold));
      
      for (int i=1;i<100;i++) {
        // setup the world
        world.command("setup");

        world.command(String.format("repeat %d [go]", steps));
        world.command("export-world \"world" + "configurations/" + world_name + format("_%04d",i) +".csv\"");

        err.println("[INFO] Saving: " + "world" + world_name + ".csv");

        world.command("clear-all");
        world.command("reset-ticks");
      }


    } catch (Exception ex) {
      ex.printStackTrace();
    }

  }

}
