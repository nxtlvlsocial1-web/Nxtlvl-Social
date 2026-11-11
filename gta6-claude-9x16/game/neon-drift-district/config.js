// PROTOTYPE - NOT FOR PRODUCTION
// Question: does drifting through neon streets and chaining combos feel fast and satisfying within the first 10 seconds?
// Date: 2026-11-11
// Every tuning value lives here, each with value, min, max and step. The game reads them live
// through tune.<name> (index.html); the tweak panel, an add-on, writes them back here.
window.CONFIG = {
  seed: 1, // every gameplay random call reads rng(), seeded from this (or ?seed= in the address)
  volume: { value: 0.5, min: 0, max: 1, step: 0.05 },

  // The car (world units are metres-ish; speeds in units per second)
  car_accel: { value: 34, min: 10, max: 80, step: 1 },          // forward acceleration, u/s^2
  car_max_speed: { value: 50, min: 20, max: 90, step: 1 },      // top speed, u/s
  car_reverse_max: { value: 14, min: 4, max: 30, step: 1 },     // top reverse speed, u/s
  car_brake: { value: 70, min: 20, max: 150, step: 1 },         // braking, u/s^2
  car_drag: { value: 0.22, min: 0, max: 1, step: 0.01 },        // air drag, fraction of speed per s
  car_turn_rate: { value: 2.7, min: 1, max: 5, step: 0.05 },    // steering, radians per s at turning speed
  car_turn_min_speed: { value: 7, min: 1, max: 20, step: 0.5 }, // speed under which steering fades out, u/s
  car_turn_highspeed_cut: { value: 0.3, min: 0, max: 0.8, step: 0.02 }, // steering lost at top speed (brake to turn tighter)
  grip: { value: 9, min: 2, max: 25, step: 0.5 },               // sideways grip, 1/s (higher = stickier)
  grip_recover: { value: 4.5, min: 1, max: 15, step: 0.5 },     // grip while a slide straightens out, 1/s

  // The drift
  drift_grip: { value: 1.3, min: 0.2, max: 6, step: 0.1 },      // sideways grip while drift is held, 1/s
  drift_turn_boost: { value: 1.5, min: 1, max: 2.5, step: 0.05 }, // extra steering while drifting
  drift_keep_speed: { value: 0.35, min: 0, max: 1, step: 0.05 },  // share of lost sideways speed given back forwards
  drift_min_speed: { value: 13, min: 4, max: 30, step: 1 },     // slower than this, no drift, u/s
  drift_min_angle: { value: 0.2, min: 0.05, max: 0.6, step: 0.01 }, // slip angle that counts as a drift, radians
  drift_points_rate: { value: 6, min: 1, max: 30, step: 1 },    // points per (u/s x radian) per s
  combo_window: { value: 2.6, min: 0.5, max: 6, step: 0.1 },    // seconds to start the next drift and keep the chain
  crash_speed: { value: 16, min: 4, max: 40, step: 1 },         // impact speed that breaks the combo, u/s

  // Jumps
  gravity: { value: 30, min: 10, max: 60, step: 1 },            // u/s^2
  air_steer: { value: 0.35, min: 0, max: 1, step: 0.05 },       // share of steering kept in the air
  air_points_rate: { value: 120, min: 0, max: 500, step: 10 },  // points per second of air
  step_up: { value: 0.8, min: 0.2, max: 2, step: 0.1 },         // highest kerb the car rolls up, u
  climb_slope: { value: 0.45, min: 0, max: 1, step: 0.05 },     // steepest ramp the car climbs (rise per unit), so the garage ramp is drivable
  slowmo_time: { value: 0.8, min: 0, max: 1.5, step: 0.05 },    // real seconds of slow motion off a big ramp launch
  slowmo_scale: { value: 0.35, min: 0.1, max: 1, step: 0.05 },  // game speed during it
  ramp_boost: { value: 1.3, min: 1, max: 2, step: 0.05 },       // street ramps throw the car this much higher
  jump_fov_kick: { value: 10, min: 0, max: 30, step: 1 },       // extra field of view at take-off, degrees

  // Drift effects
  smoke_amount: { value: 2.2, min: 0, max: 5, step: 0.1 },      // smoke puffs per rear wheel per step while sliding
  spark_rate: { value: 0.55, min: 0, max: 1, step: 0.05 },      // chance per wheel per step of a spark shower

  // Camera: the cinematic chase view (C switches to the top-down view)
  chase_dist: { value: 11, min: 4, max: 30, step: 0.5 },         // distance behind the car, u
  chase_height: { value: 5.4, min: 1.5, max: 20, step: 0.1 },   // height above the car, u
  chase_look: { value: 4, min: 0, max: 30, step: 0.5 },         // how far ahead of the car it looks, u
  chase_speed_pull: { value: 0.07, min: 0, max: 0.4, step: 0.01 }, // extra distance per u/s of speed
  chase_turn: { value: 3.2, min: 0.5, max: 12, step: 0.1 },     // how fast it swings round behind the car, 1/s
  chase_fov: { value: 58, min: 30, max: 90, step: 1 },          // vertical field of view in landscape, degrees
  chase_fov_across: { value: 62, min: 40, max: 100, step: 1 },  // narrowest view across on a tall screen, degrees
  card_time: { value: 2.6, min: 0, max: 6, step: 0.1 },         // seconds the title card shows at the start
  cam_height: { value: 62, min: 20, max: 120, step: 1 },        // camera height above the car, u
  cam_back: { value: 22, min: 0, max: 80, step: 1 },            // camera distance south of the car, u
  cam_lookahead: { value: 0.55, min: 0, max: 1.5, step: 0.05 }, // seconds of velocity the view leads by
  cam_fov: { value: 46, min: 30, max: 80, step: 1 },            // vertical field of view in landscape, degrees
  cam_speed_fov: { value: 8, min: 0, max: 25, step: 1 },        // extra field of view at top speed, degrees

  // The city
  traffic_count: { value: 26, min: 0, max: 60, step: 1 },       // traffic cars (read at start)
  traffic_speed: { value: 13, min: 4, max: 30, step: 0.5 },     // u/s
  rain_drops: { value: 1800, min: 0, max: 5000, step: 100 },    // raindrops drawn (read at start)

  // The rooftop ramp challenge
  challenge_time: { value: 60, min: 10, max: 180, step: 1 },    // seconds to reach the rooftop ramp and jump
};
