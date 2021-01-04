import { config, layoutAttributeScan } from "./config";
import scoreHtml from "./pages/score.html";
import scoreRow from "./components/score/nba/scoreRow.html";

const getScores = (container, gameKey, league) => {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      let data = null;

      data = JSON.parse(xhr.responseText).data;
      renderScores(data, container);
    }
  };

  const dt = new Date();
  const dtStr = `${dt.getFullYear()}-${dt.getMonth() + 1}-${dt.getDate()}`;
  let url = `${config.API_URL}/${league}/game/id/${gameKey}`;
  xhr.open("GET", url, true);
  xhr.send(null);
};

const renderScores = (data, container) => {
  let html = scoreHtml;

  const rows = [];
  const awayRow = renderRow(data, scoreRow, "away");
  const homeRow = renderRow(data, scoreRow, "home");

  rows.push(awayRow);
  rows.push(homeRow);

  let period = "Not Started";

  if (data.current_period === 0) {
    period = "Not Started";
  } else if (data.game_status === "Final") {
    period = "Final";
  } else {
    period = `Quarter ${data.current_period}`;
  }

  html = html.replace("[PERIOD]", period);
  html = html.replace("[SCORE_ROWS]", rows.join(""));

  container.innerHTML = html;
};

const renderRow = (data, row, pos) => {
  row = row.replace("[TEAM_LOGO]", data[`${pos}_team`].logo);
  row = row.replace("[TEAM_NAME]", data[`${pos}_team`].full_name);
  row = row.replace("[WINS]", data[`${pos}_team`].standings.wins);
  row = row.replace("[LOSSES]", data[`${pos}_team`].standings.losses);
  row = row.replace("[POS_WINS]", data[`${pos}_team`].standings[pos].wins);
  row = row.replace("[POS_LOSSES]", data[`${pos}_team`].standings[pos].losses);
  row = row.replace("[POS]", pos);

  if (data.periods[0][`${pos}_score`] > 0) {
    row = row.replace("[P1]", data.periods[0][`${pos}_score`]);
  } else {
    row = row.replace("[P1]", "-");
  }
  if (data.periods[1][`${pos}_score`] > 0) {
    row = row.replace("[P2]", data.periods[1][`${pos}_score`]);
  } else {
    row = row.replace("[P2]", "-");
  }
  if (data.periods[2][`${pos}_score`] > 0) {
    row = row.replace("[P3]", data.periods[2][`${pos}_score`]);
  } else {
    row = row.replace("[P3]", "-");
  }
  if (data.periods[3][`${pos}_score`] > 0) {
    row = row.replace("[P4]", data.periods[3][`${pos}_score`]);
  } else {
    row = row.replace("[P4]", "-");
  }

  let total = 0;
  for (let i = 0; i < data.periods.length; i++) {
    total += data.periods[i][`${pos}_score`];
  }

  if (total === 0) {
    total = "-";
  }

  row = row.replace("[TOTAL]", total);
  return row;
};

export const scanScores = () => {
  const scoreEls = document.getElementsByClassName("fs-scores-box");

  for (let i = 0; i < scoreEls.length; i++) {
    const el = scoreEls[i];
    const key = el.getAttribute("key");
    const league = el.getAttribute("league");

    layoutAttributeScan(el);

    getScores(el, key, league);
  }
};
