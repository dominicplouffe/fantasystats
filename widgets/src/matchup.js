import { config, layoutAttributeScan } from "./config";
import matchupHtml from "./pages/matchup.html";
import statsRow from "./components/matchup/nba/statsRow.html";

const getMatchup = (container, league, season, team1, team2) => {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      let data = null;

      data = JSON.parse(xhr.responseText).data;
      console.log(data);
      renderMatchup(data, container);
    }
  };

  let url = `${config.API_URL}/${league}/teams/${season}/${team1}/${team2}`;

  xhr.open("GET", url, true);
  xhr.send(null);
};

const renderMatchup = (data, container) => {
  let html = matchupHtml;

  html = html.replace("[TEAM1_NAME]", data.away.details.full_name);
  html = html.replace("[TEAM1_LOGO]", data.away.details.logo);
  html = html.replace("[TEAM2_NAME]", data.home.details.full_name);
  html = html.replace("[TEAM2_LOGO]", data.home.details.logo);

  const per_games = [];
  const perf = [];

  const per_game_names = [
    ["points_per_game", "Points"],
    ["assists_per_game", "Assists"],
    ["blocks_per_game", "Blocks"],
    ["steals_per_game", "Steals"],
    ["rebs_per_game", "Rebounds"],
    ["def_rebs_per_game", "Defensive Rebounds"],
    ["fgm_per_game", "Field Goals"],
    ["tpm_per_game", "3 Points"],
    ["ftm_per_game", "Free Throws"],
    ["fouls_per_game", "Fouls"],
  ];

  for (let i = 0; i < per_game_names.length; i++) {
    const sn = per_game_names[i];
    const key = sn[0];
    const label = sn[1];

    let rowHtml = statsRow;

    let team1_per = parseInt(
      (data.away.team_stats[key] /
        (data.away.team_stats[key] + data.home.team_stats[key])) *
        100
    );
    let team2_per = 100 - team1_per;

    rowHtml = rowHtml.replace(
      "[TEAM1_VALUE]",
      data.away.team_stats[key].toFixed(0)
    );
    rowHtml = rowHtml.replace(
      "[TEAM2_VALUE]",
      data.home.team_stats[key].toFixed(0)
    );
    rowHtml = rowHtml.replace("[TEAM1_PER]", team1_per);
    rowHtml = rowHtml.replace("[TEAM2_PER]", team2_per);
    rowHtml = rowHtml.replace("[TEAM1_COLOR]", data.away.details.color1);
    rowHtml = rowHtml.replace("[TEAM2_COLOR]", data.home.details.color1);
    rowHtml = rowHtml.replace("[STATS_NAME]", label);

    per_games.push(rowHtml);
  }

  const perf_names = [
    ["fgpct", "Field Goal %"],
    ["tppct", "3 Point Made %"],
    ["ftpct", "Free Throw Made %"],
  ];

  for (let i = 0; i < perf_names.length; i++) {
    const sn = perf_names[i];
    const key = sn[0];
    const label = sn[1];

    let rowHtml = statsRow;

    let team1_per = parseInt(
      (data.away.team_stats[key] /
        (data.away.team_stats[key] + data.home.team_stats[key])) *
        100
    );
    let team2_per = 100 - team1_per;

    rowHtml = rowHtml.replace(
      "[TEAM1_VALUE]",
      `${(data.away.team_stats[key] * 100).toFixed(0)}%`
    );
    rowHtml = rowHtml.replace(
      "[TEAM2_VALUE]",
      `${(data.home.team_stats[key] * 100).toFixed(0)}%`
    );
    rowHtml = rowHtml.replace("[TEAM1_PER]", team1_per);
    rowHtml = rowHtml.replace("[TEAM2_PER]", team2_per);
    rowHtml = rowHtml.replace("[TEAM1_COLOR]", data.away.details.color1);
    rowHtml = rowHtml.replace("[TEAM2_COLOR]", data.home.details.color1);
    rowHtml = rowHtml.replace("[STATS_NAME]", label);

    perf.push(rowHtml);
  }

  html = html.replace("[PER_GAME_ROWS]", per_games.join(""));
  html = html.replace("[PERF_ROWS]", perf.join(""));
  container.innerHTML = html;
};

export const scanMatchup = () => {
  const matchupEls = document.getElementsByClassName("fs-matchup-box");

  for (let i = 0; i < matchupEls.length; i++) {
    const el = matchupEls[i];
    const league = el.getAttribute("league");
    const team1 = el.getAttribute("team1");
    const team2 = el.getAttribute("team2");
    const season = el.getAttribute("season");

    layoutAttributeScan(el);

    getMatchup(el, league, season, team1, team2);
  }
};
