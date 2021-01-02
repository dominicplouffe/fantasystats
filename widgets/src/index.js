import { config } from "./config";
import { scanFullOdds } from "./odds";
import { scanPlayer } from "./player";
import { scanMatchup } from "./matchup";

import "./styles.css";
import "./player.css";
import "./matchup.css";

const scan = () => {
  scanFullOdds();
  scanPlayer();
  scanMatchup();
};

(function (window) {
  window.fs = {
    config: config,
    scan: scan,
  };
})(window);
