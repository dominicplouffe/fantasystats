import { config } from "./config";
import { scanFullOdds } from "./odds";
import { scanPlayer } from "./player";
import "./styles.css";
import "./player.css";

const scan = () => {
  scanFullOdds();
  scanPlayer();
};

(function (window) {
  window.fs = {
    config: config,
    scan: scan,
  };
})(window);
