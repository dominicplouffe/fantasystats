import { config, layoutAttributeScan } from "./config";
import oddsHtml from "./pages/odds.html";
import oddsRow from "./components/odds/oddsRow.html";
import teamBox from "./components/odds/teamBox.html";
import spreadCell from "./components/odds/spreadCell.html";
import totalCell from "./components/odds/totalCell.html";
import moneylineCell from "./components/odds/moneylineCell.html";

const getGameOdds = (container, gameKey, league) => {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      let gk = gameKey;

      if (!gk) {
        gk = config.GAME_KEY;
      }

      let data = null;

      if (gameKey) {
        data = [JSON.parse(xhr.responseText).data];
      } else {
        data = JSON.parse(xhr.responseText).data;
      }
      renderOdds(data, container, gk);
    }
  };

  const dt = new Date();
  const dtStr = `${dt.getFullYear()}-${dt.getMonth() + 1}-${dt.getDate()}`;
  let url = null;

  if (gameKey) {
    url = `${config.API_URL}/${league}/game/id/${gameKey}`;
  } else {
    url = `${config.API_URL}/${league}/games/date/${dtStr}`;
  }

  xhr.open("GET", url, true);
  xhr.send(null);
};

const renderOdds = (games, container, gameKey) => {
  let rows = [];
  for (let i = 0; i < games.length; i++) {
    const game = games[i];

    if (gameKey && game.game_key !== gameKey) {
      continue;
    }

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
      let odds = game.odds[bookMaker];
      newRow = renderSpread(odds, bookMaker, newRow);
      newRow = renderTotal(odds, bookMaker, newRow);
      newRow = renderMoneyLine(odds, bookMaker, newRow);
    }

    rows.push(newRow);
  }

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

  let awaySpread = "";
  let awayOdds = "";
  let homeSpread = "";
  let homeOdds = "";

  if (odds.spread) {
    awaySpread = odds.spread.away.spread;
    awayOdds = odds.spread.away.odds;

    homeSpread = odds.spread.home.spread;
    homeOdds = odds.spread.home.odds;
  }

  awaySpreadCell = awaySpreadCell.replace("[SPREAD]", awaySpread);
  awaySpreadCell = awaySpreadCell.replace("[ODDS]", awayOdds);
  awaySpreadCell = awaySpreadCell.replace("[CLASS]", awayClass);

  let homeSpeadCell = spreadCell;
  homeSpeadCell = homeSpeadCell.replace("[SPREAD]", homeSpread);
  homeSpeadCell = homeSpeadCell.replace("[ODDS]", homeOdds);
  homeSpeadCell = homeSpeadCell.replace("[CLASS]", homeClass);

  newRow = newRow.replace(`[${bookMaker}_AWAY_SPREAD]`, awaySpreadCell);
  newRow = newRow.replace(`[${bookMaker}_HOME_SPREAD]`, homeSpeadCell);

  return newRow;
};

const renderTotal = (odds, bookMaker, newRow) => {
  let overClass = "odds-box";
  let underClass = "odds-box";

  let overPoints = "";
  let overOdds = "";
  let underOdds = "";
  let underPoints = "";

  if (odds.over_under) {
    overPoints = odds.over_under.over.points;
    overOdds = odds.over_under.over.odds;
    underPoints = odds.over_under.under.points;
    underOdds = odds.over_under.under.odds;
  }

  let overCell = totalCell;
  overCell = overCell.replace("[OVER_UNDER]", `o${overPoints}`);
  overCell = overCell.replace("[ODDS]", overOdds);
  overCell = overCell.replace("[CLASS]", overClass);

  let underCell = totalCell;
  underCell = underCell.replace("[OVER_UNDER]", `u${underPoints}`);
  underCell = underCell.replace("[ODDS]", underOdds);
  underCell = underCell.replace("[CLASS]", underClass);

  newRow = newRow.replace(`[${bookMaker}_OVER]`, overCell);
  newRow = newRow.replace(`[${bookMaker}_UNDER]`, underCell);

  return newRow;
};

const renderMoneyLine = (odds, bookMaker, newRow) => {
  let awayClass = "odds-box";
  let homeClass = "odds-box";

  let moneyLineHome = "";
  let moneyLineAway = "";

  if (odds.money_line) {
    moneyLineHome = odds.money_line.home.odds;
    moneyLineAway = odds.money_line.away.odds;
  }

  let awayCell = moneylineCell;
  awayCell = awayCell.replace("[LINE]", moneyLineAway);
  awayCell = awayCell.replace("[CLASS]", awayClass);

  let homeCell = moneylineCell;
  homeCell = homeCell.replace("[LINE]", moneyLineHome);
  homeCell = homeCell.replace("[CLASS]", homeClass);

  newRow = newRow.replace(`[${bookMaker}_AWAY_LINE]`, awayCell);
  newRow = newRow.replace(`[${bookMaker}_HOME_LINE]`, homeCell);

  return newRow;
};

export const scanFullOdds = () => {
  const oddsEls = document.getElementsByClassName("fs-odds-box");

  for (let i = 0; i < oddsEls.length; i++) {
    const el = oddsEls[i];
    const key = el.getAttribute("key");
    const league = el.getAttribute("league");

    layoutAttributeScan(el);

    getGameOdds(el, key, league);
  }
};
