import org.nlogo.headless.HeadlessWorkspace;

import static java.lang.System.out;
import static java.lang.System.err;
import static java.lang.String.format;

public class CalculateMeanLiving{
  /*
   * Static variables used to redefined experiemnts.
   */
  // number of steps
  static int steps = 250;
  // number of runs
  static int runs = 200;

  // global parameters

  public static void main(String[] argv) {
    /*
     * Command line arguments.
     */
    int world_size = Integer.parseInt(argv[0]);
    int init_life = Integer.parseInt(argv[1]);
    boolean rand = Boolean.parseBoolean(argv[2]);
    boolean sync = Boolean.parseBoolean(argv[3]);
    
    int deterministic_period = Integer.parseInt(argv[4]);
    double rule_switch_prob = Double.parseDouble(argv[5]);
    int second_threshold =  Integer.parseInt(argv[6]);
    
    /*
    * Main loop. 
    */
    HeadlessWorkspace world = HeadlessWorkspace.newInstance();
    try {
      world.open("life-rule-switching.nlogo");

      //out.println("world_size,init_life,rand,sync,deterministic_period,p,second_threshold,living");
      //for (int st = second_threshold; st<=9; st++) {
      for (int runNo = 0; runNo<runs; runNo++) {
        out.println(
            format("%d,%d,%s,%s,%d,%3.2f,%d,%7.4f",
              world_size, init_life, rand, sync, 
              deterministic_period, rule_switch_prob, second_threshold,
              calcLiving(world, world_size, init_life, rand, sync, 
                deterministic_period, rule_switch_prob, second_threshold)
              )
            );
      }
      //}

      world.dispose();
    } catch (Exception ex) {
      ex.printStackTrace();
    }

  }

  private static double calcLiving(
      HeadlessWorkspace world, 
      int world_size, int init_life, boolean rand, boolean sync, 
      int deterministic_period, double rule_switch_prob, int second_threshold) {

    double living = 0.0;

    //err.println("[INFO] restaring simulation!");

    // name is build from the parsed values
    String world_name = new String();

    try {
      // load the model

      // model specific setup
      world.command(format("set world-size %d", world_size));
      //err.println(format("set world-size %d", world_size));

      world.command(format("set init-life %d", init_life));
      //err.println(format("set init-life %d", init_life));

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
        //err.println("set deterministic false");

        world.command(format("set rule-switch-prob %3.2f", rule_switch_prob)); 
        //err.println(format("set rule-switch-prob %3.2f", rule_switch_prob)); 

      } else { 
        world.command("set deterministic true");
        //err.println("set deterministic true");

        world.command(format("set deterministic-period %d", deterministic_period));
        //err.println(format("set deterministic-period %d", deterministic_period));

        world_name += "_detr"; 
        world_name += format("_dp%d", deterministic_period); 
      }

      world_name += format("_st%d", second_threshold);
      world.command(format("set second-threshold %d", second_threshold));
      //err.println(format("set second-threshold %d", second_threshold));
      
      // setup the world
      world.command("setup");
      
      // run the simulation
      world.command(String.format("repeat %d [go]", steps));
      
      // report the percentage of living cells
      living = Double.parseDouble(world.report("%living").toString());

      world.command("clear-all");
      world.command("reset-ticks");


    } catch (Exception ex) {
      ex.printStackTrace();
    }

    return living;

  }

}
