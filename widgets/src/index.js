import { config } from "./config";
import { scanFullOdds } from "./odds";
import { scanPlayer } from "./player";
import { scanMatchup } from "./matchup";
import { scanScores } from "./score";

import "./css/styles.css";
import "./css/odds.css";
import "./css/player.css";
import "./css/matchup.css";
import "./css/score.css";

const scan = () => {
  scanFullOdds();
  scanPlayer();
  scanMatchup();
  scanScores();
};

(function (window) {
  window.fs = {
    config: config,
    scan: scan,
  };
})(window);
