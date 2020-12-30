import "./styles.css";
import oddsHtml from "./pages/odds.html";
import oddsRow from "./components/odds/oddsRow.html";
import teamBox from "./components/odds/teamBox.html";
import spreadCell from "./components/odds/spreadCell.html";
import totalCell from "./components/odds/totalCell.html";
import moneylineCell from "./components/odds/moneylineCell.html";

const LEAGUE = "nba";
const API_URL = `http://localhost:5000/${LEAGUE}/`;

const getGameOdds = () => {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      renderOdds(JSON.parse(xhr.responseText).data);
    }
  };

  const dt = new Date();
  const dtStr = `${dt.getFullYear()}-${dt.getMonth() + 1}-${dt.getDate()}`;
  const url = `${API_URL}/games/date/${dtStr}`;

  xhr.open("GET", url, true);
  xhr.send(null);
};

const renderOdds = (games) => {
  let rows = [];
  for (let i = 0; i < games.length; i++) {
    const game = games[i];

    const startTime = new Date(game.start_time);
    let startHour = startTime.getUTCHours();
    let startMinute = startTime.getUTCMinutes();
    if (startHour > 12) {
      startHour = startHour - 12;
    }
    if (startMinute.toString().length === 1) {
      startMinute = `${startMinute}0`;
    }

    // Replace the Team info
    let newRow = oddsRow;

    let teamInfo = teamBox;
    teamInfo = teamInfo.replace("[AWAY_ABBR]", game.away_team.abbr);
    teamInfo = teamInfo.replace("[AWAY_LOGO]", game.away_team.logo);

    teamInfo = teamInfo.replace("[HOME_ABBR]", game.home_team.abbr);
    teamInfo = teamInfo.replace("[HOME_LOGO]", game.home_team.logo);

    teamInfo = teamInfo.replace("[HOURS]", `${startHour}:${startMinute}`);
    newRow = newRow.replace("[TEAM-BOX]", teamInfo);

    // Replace the spread
    for (let bookMaker in game.odds) {
      const odds = game.odds[bookMaker];

      newRow = renderSpread(odds, bookMaker, newRow);
      newRow = renderTotal(odds, bookMaker, newRow);
      newRow = renderMoneyLine(odds, bookMaker, newRow);
    }

    rows.push(newRow);
  }

  const container = document.getElementById("container");
  container.innerHTML = oddsHtml.replace("[ODDS_ROWS]", rows.join(""));

  const dd = document.getElementById("odds-choice");
  dd.addEventListener("change", (e) => {
    const els = document.getElementsByClassName("fs-odds");

    for (let i = 0; i < els.length; i++) {
      const el = els[i];
      if (el.className.indexOf("hide") === -1) {
        el.className = `${el.className} hide`;
      }

      if (el.className.indexOf(`fs-${dd.value}`) > -1) {
        el.className = el.className.replace(" hide", "");
      }
    }
  });
};

const renderSpread = (odds, bookMaker, newRow) => {
  let awayClass = "odds-box";
  let homeClass = "odds-box";

  let awaySpreadCell = spreadCell;
  awaySpreadCell = awaySpreadCell.replace("[SPREAD]", odds.spread.away.spread);
  awaySpreadCell = awaySpreadCell.replace("[ODDS]", odds.spread.away.odds);
  awaySpreadCell = awaySpreadCell.replace("[CLASS]", awayClass);

  let homeSpeadCell = spreadCell;
  homeSpeadCell = homeSpeadCell.replace("[SPREAD]", odds.spread.home.spread);
  homeSpeadCell = homeSpeadCell.replace("[ODDS]", odds.spread.home.odds);
  homeSpeadCell = homeSpeadCell.replace("[CLASS]", homeClass);

  newRow = newRow.replace(`[${bookMaker}_AWAY_SPREAD]`, awaySpreadCell);
  newRow = newRow.replace(`[${bookMaker}_HOME_SPREAD]`, homeSpeadCell);

  return newRow;
};

const renderTotal = (odds, bookMaker, newRow) => {
  let overClass = "odds-box";
  let underClass = "odds-box";

  let overCell = totalCell;
  overCell = overCell.replace(
    "[OVER_UNDER]",
    `o${odds.over_under.over.points}`
  );
  overCell = overCell.replace("[ODDS]", odds.over_under.over.odds);
  overCell = overCell.replace("[CLASS]", overClass);

  let underCell = totalCell;
  underCell = underCell.replace(
    "[OVER_UNDER]",
    `u${odds.over_under.under.points}`
  );
  underCell = underCell.replace("[ODDS]", odds.over_under.under.odds);
  underCell = underCell.replace("[CLASS]", underClass);

  newRow = newRow.replace(`[${bookMaker}_OVER]`, overCell);
  newRow = newRow.replace(`[${bookMaker}_UNDER]`, underCell);

  return newRow;
};

const renderMoneyLine = (odds, bookMaker, newRow) => {
  let awayClass = "odds-box";
  let homeClass = "odds-box";

  let awayCell = moneylineCell;
  awayCell = awayCell.replace("[LINE]", odds.money_line.away.odds);
  awayCell = awayCell.replace("[CLASS]", awayClass);

  let homeCell = moneylineCell;
  homeCell = homeCell.replace("[LINE]", odds.money_line.home.odds);
  homeCell = homeCell.replace("[CLASS]", homeClass);

  newRow = newRow.replace(`[${bookMaker}_AWAY_LINE]`, awayCell);
  newRow = newRow.replace(`[${bookMaker}_HOME_LINE]`, homeCell);

  return newRow;
};

(function (window) {
  getGameOdds();
})(window);
