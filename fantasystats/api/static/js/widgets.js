!function(e){var t={};function n(a){if(t[a])return t[a].exports;var o=t[a]={i:a,l:!1,exports:{}};return e[a].call(o.exports,o,o.exports,n),o.l=!0,o.exports}n.m=e,n.c=t,n.d=function(e,t,a){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(a,o,function(t){return e[t]}.bind(null,o));return a},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=18)}([function(e,t,n){"use strict";e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var n=function(e,t){var n=e[1]||"",a=e[3];if(!a)return n;if(t&&"function"==typeof btoa){var o=(s=a,l=btoa(unescape(encodeURIComponent(JSON.stringify(s)))),d="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(l),"/*# ".concat(d," */")),r=a.sources.map((function(e){return"/*# sourceURL=".concat(a.sourceRoot||"").concat(e," */")}));return[n].concat(r).concat([o]).join("\n")}var s,l,d;return[n].join("\n")}(t,e);return t[2]?"@media ".concat(t[2]," {").concat(n,"}"):n})).join("")},t.i=function(e,n,a){"string"==typeof e&&(e=[[null,e,""]]);var o={};if(a)for(var r=0;r<this.length;r++){var s=this[r][0];null!=s&&(o[s]=!0)}for(var l=0;l<e.length;l++){var d=[].concat(e[l]);a&&o[d[0]]||(n&&(d[2]?d[2]="".concat(n," and ").concat(d[2]):d[2]=n),t.push(d))}},t}},function(e,t,n){"use strict";var a,o=function(){return void 0===a&&(a=Boolean(window&&document&&document.all&&!window.atob)),a},r=function(){var e={};return function(t){if(void 0===e[t]){var n=document.querySelector(t);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}e[t]=n}return e[t]}}(),s=[];function l(e){for(var t=-1,n=0;n<s.length;n++)if(s[n].identifier===e){t=n;break}return t}function d(e,t){for(var n={},a=[],o=0;o<e.length;o++){var r=e[o],d=t.base?r[0]+t.base:r[0],i=n[d]||0,c="".concat(d," ").concat(i);n[d]=i+1;var p=l(c),u={css:r[1],media:r[2],sourceMap:r[3]};-1!==p?(s[p].references++,s[p].updater(u)):s.push({identifier:c,updater:m(u,t),references:1}),a.push(c)}return a}function i(e){var t=document.createElement("style"),a=e.attributes||{};if(void 0===a.nonce){var o=n.nc;o&&(a.nonce=o)}if(Object.keys(a).forEach((function(e){t.setAttribute(e,a[e])})),"function"==typeof e.insert)e.insert(t);else{var s=r(e.insert||"head");if(!s)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");s.appendChild(t)}return t}var c,p=(c=[],function(e,t){return c[e]=t,c.filter(Boolean).join("\n")});function u(e,t,n,a){var o=n?"":a.media?"@media ".concat(a.media," {").concat(a.css,"}"):a.css;if(e.styleSheet)e.styleSheet.cssText=p(t,o);else{var r=document.createTextNode(o),s=e.childNodes;s[t]&&e.removeChild(s[t]),s.length?e.insertBefore(r,s[t]):e.appendChild(r)}}function g(e,t,n){var a=n.css,o=n.media,r=n.sourceMap;if(o?e.setAttribute("media",o):e.removeAttribute("media"),r&&"undefined"!=typeof btoa&&(a+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(r))))," */")),e.styleSheet)e.styleSheet.cssText=a;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(a))}}var f=null,_=0;function m(e,t){var n,a,o;if(t.singleton){var r=_++;n=f||(f=i(t)),a=u.bind(null,n,r,!1),o=u.bind(null,n,r,!0)}else n=i(t),a=g.bind(null,n,t),o=function(){!function(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e)}(n)};return a(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap)return;a(e=t)}else o()}}e.exports=function(e,t){(t=t||{}).singleton||"boolean"==typeof t.singleton||(t.singleton=o());var n=d(e=e||[],t);return function(e){if(e=e||[],"[object Array]"===Object.prototype.toString.call(e)){for(var a=0;a<n.length;a++){var o=l(n[a]);s[o].references--}for(var r=d(e,t),i=0;i<n.length;i++){var c=l(n[i]);0===s[c].references&&(s[c].updater(),s.splice(c,1))}n=r}}}},function(e,t){e.exports='<div class="[CLASS] fs-spread fs-odds" style="padding-top:5px;padding-bottom:5px"> [SPREAD]<br/> [ODDS] </div>'},function(e,t){e.exports='<div class="[CLASS] hide fs-total fs-odds" style="padding-top:5px;padding-bottom:5px"> [OVER_UNDER]<br/> [ODDS] </div>'},function(e,t){e.exports='<div class="[CLASS] fs-moneyline hide fs-odds" style="padding-top:15px;padding-bottom:15px"> [LINE] </div>'},function(e,t){e.exports='<tr> <td><strong>[TEAM1_VALUE]</strong></td> <td><small>[STATS_NAME]</small></td> <td><strong>[TEAM2_VALUE]</strong></td> </tr> <tr> <td colspan="3"> <div class="team1-col team-stats" style="width:[TEAM1_PER]%;background-color:[TEAM1_COLOR];height:10px"></div> <div class="team2-col team-stats" style="width:[TEAM2_PER]%;background-color:[TEAM2_COLOR];height:10px"></div> </td> </tr>'},function(e,t){e.exports='<div class="odds-selection"> Choose Your Odds: <select name="odds-choice" id="odds-choice" class="odds-choice"> <option value="spread">Spread</option> <option value="moneyline">Moneyline</option> <option value="total">Over/Under</option> </select> </div> <table class="odds-table"> <thead> <th style="width:22%"><strong>Game</strong></th> <th style="width:13%"><strong>Draftkings</strong></th> <th style="width:13%"><strong>FanDuel</strong></th> <th style="width:13%"><strong>Sugar House</strong></th> <th style="width:13%"><strong>BetMGM</strong></th> <th style="width:13%"><strong>Unibet</strong></th> <th style="width:13%"><strong>Pointsbet</strong></th> </thead> <tbody> [ODDS_ROWS] </tbody> </table>'},function(e,t){e.exports="<tr> <td>[TEAM-BOX]</td> <td> [DraftKings_AWAY_SPREAD] [DraftKings_HOME_SPREAD] [DraftKings_OVER] [DraftKings_UNDER] [DraftKings_AWAY_LINE] [DraftKings_HOME_LINE] </td> <td> [FanDuel_AWAY_SPREAD] [FanDuel_HOME_SPREAD] [FanDuel_OVER] [FanDuel_UNDER] [FanDuel_AWAY_LINE] [FanDuel_HOME_LINE] </td> <td> [Sugarhouse_AWAY_SPREAD] [Sugarhouse_HOME_SPREAD] [Sugarhouse_OVER] [Sugarhouse_UNDER] [Sugarhouse_AWAY_LINE] [Sugarhouse_HOME_LINE] </td> <td> [BetMGM_AWAY_SPREAD] [BetMGM_HOME_SPREAD] [BetMGM_OVER] [BetMGM_UNDER] [BetMGM_AWAY_LINE] [BetMGM_HOME_LINE] </td> <td> [Unibet_AWAY_SPREAD] [Unibet_HOME_SPREAD] [Unibet_OVER] [Unibet_UNDER] [Unibet_AWAY_LINE] [Unibet_HOME_LINE] </td> <td> [PointsBet_AWAY_SPREAD] [PointsBet_HOME_SPREAD] [PointsBet_OVER] [PointsBet_UNDER] [PointsBet_AWAY_LINE] [PointsBet_HOME_LINE] </td> </tr>"},function(e,t){e.exports='<div class="team-box"> <div class="time-box"> <strong>[HOURS]</strong><br/> <small>PM EST</small> </div> <div class="vs-box"> <div class="team-logo"> <img src="[AWAY_LOGO]" class="logo"/> [AWAY_ABBR] </div> <div class="team-logo"> <img src="[HOME_LOGO]" class="logo"/> [HOME_ABBR] </div> </div> </div>'},function(e,t){e.exports='<table class="player-table"> <tr> <td class="left"> <img src="[PLAYER_IMG]" class="player-img"/> </td> <td style="text-align:center"> <h4 class="player-name"> [PLAYER_NAME] <span class="player-number">[PLAYER_NUMER]</span> </h4> <div> <table class="player-stats-table"> <tr> <td><strong>Position(s)</strong><br/>[PLAYER_POS]</td> <td><strong>Weight</strong><br/>[PLAYER_WEIGHT]</td> <td><strong>Height</strong><br/>[PLAYER_HEIGHT]</td> </tr> </table> </div> </td> <td class="right"> <img src="[TEAM_LOGO]" class="player-img"/> </td> </tr> </table> <table class="player-stats-table"> <thead> <tr> <th>Year</th> <th>GP</th> <th>FG%</th> <th>3P%</th> <th>FT%</th> <th>Points</th> <th>Assists</th> <th>Steals</th> </tr> </thead> <tbody> [STATS] </tbody> </table>'},function(e,t){e.exports="<tr> <td>[YEAR]</td> <td>[GP]</td> <td>[FGP]%</td> <td>[TPP]%</td> <td>[FTP]%</td> <td>[POINTS] <small>([PPG])</small></td> <td>[ASSISTS] <small>([APG])</small></td> <td>[STEALS] <small>([SPG])</small></td> </tr>"},function(e,t){e.exports='<table class="matchup-table"> <tr> <td class="team1-col"> <img src="[TEAM1_LOGO]" class="team-img"/> <br/> <strong> [TEAM1_NAME] </strong> </td> <td> <strong>Matchup</strong> </td> <td class="team2-col"> <img src="[TEAM2_LOGO]" class="team-img"/> <br/> <strong>[TEAM2_NAME]</strong> </td> </tr> <tr> <td style="padding-top:20px">Away</td> <td style="padding-top:20px"><strong>Performance Matchup</strong></td> <td style="padding-top:20px">Home</td> </tr> [PERF_ROWS] <tr> <td style="padding-top:20px">Away</td> <td style="padding-top:20px"><strong>Per Game Matchup</strong></td> <td style="padding-top:20px">Home</td> </tr> [PER_GAME_ROWS] </table>'},function(e,t,n){var a=n(1),o=n(13);"string"==typeof(o=o.__esModule?o.default:o)&&(o=[[e.i,o,""]]);var r={insert:"head",singleton:!1};a(o,r);e.exports=o.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a)()(!1);o.push([e.i,".hide {\n    display: none;\n}\n\n.odds-selection {\n    color: #333333;\n    font-size: 15px;\n    font-size: 0.9375rem;\n    font-family: 'Oxygen', Tahoma, Arial;\n    padding: 10px;\n    margin-bottom: 20px;\n    background-color: #ecf0f2;\n    border-radius: 3px;\n}\n\n.odds-choice {\n    font-family: 'Oxygen', Tahoma, Arial;\n    padding: 5px;\n    border-radius: 3px;\n}\n\n.odds-table {\n    color: #333333;\n    font-size: 15px;\n    font-size: 0.9375rem;\n    font-family: 'Oxygen', Tahoma, Arial;\n    /* line-height: 1.75; */\n    width: 100%;\n    border-spacing: 0;\n}\n\n.odds-table th {\n    border: 0;\n    padding: 15px 5px 15px 5px;\n}\n\n\n.odds-table td {\n    border: 0;\n    border-top: 1px solid #ecf0f2 ;\n    padding: 15px 5px 15px 5px;\n}\n\n.odds-table .team-box {\n    padding: 20px 10px 20px 10px\n}\n\n.odds-table .team-box .time-box {\n    float: left;\n    padding-right: 10px;\n    padding-top: 8px;\n}\n\n.vs-box {\n    float: left;\n}\n\n.vs-box .team-logo {\n    padding-bottom: 10px;\n}\n\n.vs-box .logo {\n    max-width: 30px;\n    vertical-align: middle;\n}\n\n.odds-table .odds-box {\n    border: 1px solid #d4d8d9;\n    background-color: #ecf0f2;\n    width: 100%;\n    line-height: 1.75;\n    text-align: center;\n    font-size: 0.75rem;\n    margin-bottom: 5px;\n    border-radius: 3px;\n}\n\n.odds-table .best {\n    background-color: #bae4f7;\n    border: 2px solid #1685b5;\n\n}\n\n.team-img  {\n    width: 100px;\n    border-radius: 20px;\n    border: 1px solid #d4d8d9;\n    padding: 5px;\n    background-color: #fff;\n}",""]),t.default=o},function(e,t,n){var a=n(1),o=n(15);"string"==typeof(o=o.__esModule?o.default:o)&&(o=[[e.i,o,""]]);var r={insert:"head",singleton:!1};a(o,r);e.exports=o.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a)()(!1);o.push([e.i,".fs-player-box {\n    width: 500px;\n    border: 1px solid #ecf0f2;\n    border-radius: 3px;\n    padding: 5px;\n    background-color: #ecf0f2;\n    margin: auto;\n}\n.player-table {\n    color: #333333;\n    font-size: 15px;\n    font-size: 0.9375rem;\n    font-family: 'Oxygen', Tahoma, Arial;\n    /* line-height: 1.75; */\n    width: 100%;\n    border-spacing: 0;\n}\n\n.player-table td {\n    border: 0;\n    padding: 15px 5px 15px 5px;\n}\n\n.player-table .left {\n    width: 100px;\n}\n.player-table .right {\n    width: 100px;\n    text-align: right;\n}\n\n.player-img  {\n    width: 100px;\n    border-radius: 20px;\n    border: 1px solid #d4d8d9;\n    padding: 5px;\n    background-color: #fff;\n}\n\n.player-name {\n    font-size: 17px;\n    font-weight: bold;\n}\n\n.player-number {\n    font-size: 15px;\n    background-color: #333333;\n    color: #fff;\n    padding: 0px 3px 0px 3px;\n    border: 1px solid #fff;\n    border-radius: 5px;\n}\n\n.player-stats-table {\n    width: 100%;\n    padding: 0;\n    margin: 0;\n}\n\n.player-stats-table th {\n    padding: 0;\n    margin: 0;\n    font-size: 12px;\n    text-align: center;\n    font-weight: bold;\n}\n\n.player-stats-table td {\n    padding: 0;\n    margin: 0;\n    font-size: 12px;\n    text-align: center;\n}",""]),t.default=o},function(e,t,n){var a=n(1),o=n(17);"string"==typeof(o=o.__esModule?o.default:o)&&(o=[[e.i,o,""]]);var r={insert:"head",singleton:!1};a(o,r);e.exports=o.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a)()(!1);o.push([e.i,".fs-matchup-box {\n    width: 100%;\n    max-width: 1200px;\n    border: 1px solid #ecf0f2;\n    border-radius: 3px;\n    padding: 10px;\n    background-color: #ecf0f2;\n    margin: auto;\n}\n\n.matchup-table {\n    width: 100%;\n}\n\n.matchup-table td {\n    border: 0;\n    text-align: center;\n    padding-top: 8px;\n}\n\n\n\n.team-stats {\n    float: left;\n}\n",""]),t.default=o},function(e,t,n){"use strict";n.r(t);const a={GAME_KEY:null,API_URL:"http://localhost:5000/"};var o=n(6),r=n.n(o),s=n(7),l=n.n(s),d=n(8),i=n.n(d),c=n(2),p=n.n(c),u=n(3),g=n.n(u),f=n(4),_=n.n(f);const m=(e,t,n)=>{var o=new XMLHttpRequest;o.onreadystatechange=function(){if(o.readyState==XMLHttpRequest.DONE){let n=t;n||(n=a.GAME_KEY);let r=null;r=t?[JSON.parse(o.responseText).data]:JSON.parse(o.responseText).data,h(r,e,n)}};const r=new Date,s=`${r.getFullYear()}-${r.getMonth()+1}-${r.getDate()}`;let l=null;l=t?`${a.API_URL}/${n}/game/id/${t}`:`${a.API_URL}/${n}/games/date/${s}`,o.open("GET",l,!0),o.send(null)},h=(e,t,n)=>{let a=[];for(let t=0;t<e.length;t++){const o=e[t];if(n&&o.game_key!==n)continue;const r=new Date(o.start_time);let s=r.getUTCHours(),d=r.getUTCMinutes();s>12&&(s-=12),1===d.toString().length&&(d+="0");let c=l.a,p=i.a;p=p.replace("[AWAY_ABBR]",o.away_team.abbr),p=p.replace("[AWAY_LOGO]",o.away_team.logo),p=p.replace("[HOME_ABBR]",o.home_team.abbr),p=p.replace("[HOME_LOGO]",o.home_team.logo),p=p.replace("[HOURS]",`${s}:${d}`),c=c.replace("[TEAM-BOX]",p);for(let e in o.odds){let t=o.odds[e];c=b(t,e,c),c=E(t,e,c),c=A(t,e,c)}a.push(c)}t.innerHTML=r.a.replace("[ODDS_ROWS]",a.join(""));const o=document.getElementById("odds-choice");o.addEventListener("change",e=>{const t=document.getElementsByClassName("fs-odds");for(let e=0;e<t.length;e++){const n=t[e];-1===n.className.indexOf("hide")&&(n.className=n.className+" hide"),n.className.indexOf("fs-"+o.value)>-1&&(n.className=n.className.replace(" hide",""))}})},b=(e,t,n)=>{let a=p.a,o="",r="",s="",l="";e.spread&&(o=e.spread.away.spread,r=e.spread.away.odds,s=e.spread.home.spread,l=e.spread.home.odds),a=a.replace("[SPREAD]",o),a=a.replace("[ODDS]",r),a=a.replace("[CLASS]","odds-box");let d=p.a;return d=d.replace("[SPREAD]",s),d=d.replace("[ODDS]",l),d=d.replace("[CLASS]","odds-box"),n=(n=n.replace(`[${t}_AWAY_SPREAD]`,a)).replace(`[${t}_HOME_SPREAD]`,d)},E=(e,t,n)=>{let a="",o="",r="",s="";e.over_under&&(a=e.over_under.over.points,o=e.over_under.over.odds,s=e.over_under.under.points,r=e.over_under.under.odds);let l=g.a;l=l.replace("[OVER_UNDER]","o"+a),l=l.replace("[ODDS]",o),l=l.replace("[CLASS]","odds-box");let d=g.a;return d=d.replace("[OVER_UNDER]","u"+s),d=d.replace("[ODDS]",r),d=d.replace("[CLASS]","odds-box"),n=(n=n.replace(`[${t}_OVER]`,l)).replace(`[${t}_UNDER]`,d)},A=(e,t,n)=>{let a="",o="";e.money_line&&(a=e.money_line.home.odds,o=e.money_line.away.odds);let r=_.a;r=r.replace("[LINE]",o),r=r.replace("[CLASS]","odds-box");let s=_.a;return s=s.replace("[LINE]",a),s=s.replace("[CLASS]","odds-box"),n=(n=n.replace(`[${t}_AWAY_LINE]`,r)).replace(`[${t}_HOME_LINE]`,s)};var x=n(9),y=n.n(x),M=n(10),S=n.n(M);const v=(e,t,n)=>{var o=new XMLHttpRequest;o.onreadystatechange=function(){if(o.readyState==XMLHttpRequest.DONE){let n=t;n||(n=a.GAME_KEY);let r=null;r=JSON.parse(o.responseText).data,O(r,e)}};const r=new Date;r.getFullYear(),r.getMonth(),r.getDate();let s=`${a.API_URL}/${n}/player/${t}`;o.open("GET",s,!0),o.send(null)},O=(e,t)=>{let n=y.a;n=n.replace("[PLAYER_IMG]",e.bio.headshot),n=n.replace("[PLAYER_NAME]",e.bio.name),n=n.replace("[PLAYER_NUMER]",e.bio.primary_number),n=n.replace("[PLAYER_POS]",e.bio.position),n=e.bio.weight?n.replace("[PLAYER_WEIGHT]",e.bio.weight+"lbs"):n.replace("[PLAYER_WEIGHT]","n/a"),n=e.bio.height?n.replace("[PLAYER_HEIGHT]",e.bio.height):n.replace("[PLAYER_HEIGHT]","n/a"),n=n.replace("[TEAM_LOGO]",e.team.logo);const a=[];for(let t in e.seasons){let n=S.a;const o=e.seasons[t];n=n.replace("[YEAR]",t),n=n.replace("[GP]",o.games_played),n=n.replace("[FGP]",(100*o.fgpct).toFixed(0)),n=n.replace("[TPP]",(100*o.tppct).toFixed(0)),n=n.replace("[FTP]",(100*o.ftpct).toFixed(0)),n=n.replace("[POINTS]",o.points),n=n.replace("[ASSISTS]",o.assists),n=n.replace("[STEALS]",o.steals),n=n.replace("[PPG]",o.points_per_game.toFixed(2)),n=n.replace("[APG]",o.assists_per_game.toFixed(2)),n=n.replace("[SPG]",o.steals_per_game.toFixed(2)),a.push(n)}a.reverse(),n=n.replace("[STATS]",a.join("")),t.innerHTML=n};var R=n(11),P=n.n(R),T=n(5),L=n.n(T);const D=(e,t,n,o,r)=>{var s=new XMLHttpRequest;s.onreadystatechange=function(){if(s.readyState==XMLHttpRequest.DONE){let t=null;t=JSON.parse(s.responseText).data,console.log(t),w(t,e)}};let l=`${a.API_URL}/${t}/teams/${n}/${o}/${r}`;console.log(l),s.open("GET",l,!0),s.send(null)},w=(e,t)=>{let n=P.a;n=n.replace("[TEAM1_NAME]",e.away.details.full_name),n=n.replace("[TEAM1_LOGO]",e.away.details.logo),n=n.replace("[TEAM2_NAME]",e.home.details.full_name),n=n.replace("[TEAM2_LOGO]",e.home.details.logo);const a=[],o=[],r=[["points_per_game","Points"],["assists_per_game","Assists"],["blocks_per_game","Blocks"],["steals_per_game","Steals"],["rebs_per_game","Rebounds"],["def_rebs_per_game","Defensive Rebounds"],["fgm_per_game","Field Goals"],["tpm_per_game","3 Points"],["ftm_per_game","Free Throws"],["fouls_per_game","Fouls"]];for(let t=0;t<r.length;t++){const n=r[t],o=n[0],s=n[1];let l=L.a,d=parseInt(e.away.team_stats[o]/(e.away.team_stats[o]+e.home.team_stats[o])*100),i=100-d;l=l.replace("[TEAM1_VALUE]",e.away.team_stats[o].toFixed(0)),l=l.replace("[TEAM2_VALUE]",e.home.team_stats[o].toFixed(0)),l=l.replace("[TEAM1_PER]",d),l=l.replace("[TEAM2_PER]",i),l=l.replace("[TEAM1_COLOR]",e.away.details.color1),l=l.replace("[TEAM2_COLOR]",e.home.details.color1),l=l.replace("[STATS_NAME]",s),a.push(l)}const s=[["fgpct","Field Goal %"],["tppct","3 Point Made %"],["ftpct","Free Throw Made %"]];for(let t=0;t<s.length;t++){const n=s[t],a=n[0],r=n[1];let l=L.a,d=parseInt(e.away.team_stats[a]/(e.away.team_stats[a]+e.home.team_stats[a])*100),i=100-d;l=l.replace("[TEAM1_VALUE]",(100*e.away.team_stats[a]).toFixed(0)+"%"),l=l.replace("[TEAM2_VALUE]",(100*e.home.team_stats[a]).toFixed(0)+"%"),l=l.replace("[TEAM1_PER]",d),l=l.replace("[TEAM2_PER]",i),l=l.replace("[TEAM1_COLOR]",e.away.details.color1),l=l.replace("[TEAM2_COLOR]",e.home.details.color1),l=l.replace("[STATS_NAME]",r),o.push(l)}n=n.replace("[PER_GAME_ROWS]",a.join("")),n=n.replace("[PERF_ROWS]",o.join("")),t.innerHTML=n};n(12),n(14),n(16);const N=()=>{(()=>{const e=document.getElementsByClassName("fs-odds-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("key"),o=n.getAttribute("league");m(n,a,o)}})(),(()=>{const e=document.getElementsByClassName("fs-player-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("key"),o=n.getAttribute("league");v(n,a,o)}})(),(()=>{const e=document.getElementsByClassName("fs-matchup-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("league"),o=n.getAttribute("team1"),r=n.getAttribute("team2"),s=n.getAttribute("season");D(n,a,s,o,r)}})()};!function(e){e.fs={config:a,scan:N}}(window)}]);