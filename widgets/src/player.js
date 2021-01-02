import { config } from "./config";
import playerHtml from "./pages/player.html";
import statsRow from "./components/player/nba/statsRow.html";

const getPlayer = (container, playerKey, league) => {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      let gk = playerKey;

      if (!gk) {
        gk = config.GAME_KEY;
      }

      let data = null;

      data = JSON.parse(xhr.responseText).data;
      console.log(data);
      renderPlayer(data, container);
    }
  };

  const dt = new Date();
  const dtStr = `${dt.getFullYear()}-${dt.getMonth() + 1}-${dt.getDate()}`;
  let url = `${config.API_URL}/${league}/player/${playerKey}`;
  console.log(url);

  xhr.open("GET", url, true);
  xhr.send(null);
};

const renderPlayer = (data, container) => {
  let html = playerHtml;

  html = html.replace("[PLAYER_IMG]", data.bio.headshot);
  html = html.replace("[PLAYER_NAME]", data.bio.name);
  html = html.replace("[PLAYER_NUMER]", data.bio.primary_number);
  html = html.replace("[PLAYER_POS]", data.bio.primary_number);
  if (data.bio.weight) {
    html = html.replace("[PLAYER_WEIGHT]", `${data.bio.weight}lbs`);
  } else {
    html = html.replace("[PLAYER_WEIGHT]", `n/a`);
  }
  if (data.bio.height) {
    html = html.replace("[PLAYER_HEIGHT]", data.bio.height);
  } else {
    html = html.replace("[PLAYER_HEIGHT]", "n/a");
  }
  html = html.replace("[TEAM_LOGO]", data.team.logo);

  const stats = [];

  for (let season in data.seasons) {
    let sr = statsRow;
    const s = data.seasons[season];
    console.log(s);
    sr = sr.replace("[YEAR]", season);
    sr = sr.replace("[GP]", s.games_played);
    sr = sr.replace("[FGP]", (s.fgpct * 100).toFixed(0));
    sr = sr.replace("[TPP]", (s.tppct * 100).toFixed(0));
    sr = sr.replace("[FTP]", (s.ftpct * 100).toFixed(0));

    sr = sr.replace("[POINTS]", s.points);
    sr = sr.replace("[ASSISTS]", s.assists);
    sr = sr.replace("[STEALS]", s.steals);
    sr = sr.replace("[PPG]", s.points_per_game.toFixed(2));
    sr = sr.replace("[APG]", s.assists_per_game.toFixed(2));
    sr = sr.replace("[SPG]", s.steals_per_game.toFixed(2));

    stats.push(sr);
  }

  stats.reverse();

  html = html.replace("[STATS]", stats.join(""));

  container.innerHTML = html;
};

export const scanPlayer = () => {
  const playerEls = document.getElementsByClassName("fs-player-box");

  for (let i = 0; i < playerEls.length; i++) {
    const el = playerEls[i];
    const key = el.getAttribute("key");
    const league = el.getAttribute("league");

    getPlayer(el, key, league);
  }
};
