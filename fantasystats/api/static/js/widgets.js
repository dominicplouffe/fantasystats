!function(e){var t={};function n(a){if(t[a])return t[a].exports;var r=t[a]={i:a,l:!1,exports:{}};return e[a].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,a){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(a,r,function(t){return e[t]}.bind(null,r));return a},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=24)}([function(e,t,n){"use strict";e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var n=function(e,t){var n=e[1]||"",a=e[3];if(!a)return n;if(t&&"function"==typeof btoa){var r=(s=a,l=btoa(unescape(encodeURIComponent(JSON.stringify(s)))),d="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(l),"/*# ".concat(d," */")),o=a.sources.map((function(e){return"/*# sourceURL=".concat(a.sourceRoot||"").concat(e," */")}));return[n].concat(o).concat([r]).join("\n")}var s,l,d;return[n].join("\n")}(t,e);return t[2]?"@media ".concat(t[2]," {").concat(n,"}"):n})).join("")},t.i=function(e,n,a){"string"==typeof e&&(e=[[null,e,""]]);var r={};if(a)for(var o=0;o<this.length;o++){var s=this[o][0];null!=s&&(r[s]=!0)}for(var l=0;l<e.length;l++){var d=[].concat(e[l]);a&&r[d[0]]||(n&&(d[2]?d[2]="".concat(n," and ").concat(d[2]):d[2]=n),t.push(d))}},t}},function(e,t,n){"use strict";var a,r=function(){return void 0===a&&(a=Boolean(window&&document&&document.all&&!window.atob)),a},o=function(){var e={};return function(t){if(void 0===e[t]){var n=document.querySelector(t);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}e[t]=n}return e[t]}}(),s=[];function l(e){for(var t=-1,n=0;n<s.length;n++)if(s[n].identifier===e){t=n;break}return t}function d(e,t){for(var n={},a=[],r=0;r<e.length;r++){var o=e[r],d=t.base?o[0]+t.base:o[0],i=n[d]||0,c="".concat(d," ").concat(i);n[d]=i+1;var p=l(c),u={css:o[1],media:o[2],sourceMap:o[3]};-1!==p?(s[p].references++,s[p].updater(u)):s.push({identifier:c,updater:_(u,t),references:1}),a.push(c)}return a}function i(e){var t=document.createElement("style"),a=e.attributes||{};if(void 0===a.nonce){var r=n.nc;r&&(a.nonce=r)}if(Object.keys(a).forEach((function(e){t.setAttribute(e,a[e])})),"function"==typeof e.insert)e.insert(t);else{var s=o(e.insert||"head");if(!s)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");s.appendChild(t)}return t}var c,p=(c=[],function(e,t){return c[e]=t,c.filter(Boolean).join("\n")});function u(e,t,n,a){var r=n?"":a.media?"@media ".concat(a.media," {").concat(a.css,"}"):a.css;if(e.styleSheet)e.styleSheet.cssText=p(t,r);else{var o=document.createTextNode(r),s=e.childNodes;s[t]&&e.removeChild(s[t]),s.length?e.insertBefore(o,s[t]):e.appendChild(o)}}function g(e,t,n){var a=n.css,r=n.media,o=n.sourceMap;if(r?e.setAttribute("media",r):e.removeAttribute("media"),o&&"undefined"!=typeof btoa&&(a+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")),e.styleSheet)e.styleSheet.cssText=a;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(a))}}var f=null,m=0;function _(e,t){var n,a,r;if(t.singleton){var o=m++;n=f||(f=i(t)),a=u.bind(null,n,o,!1),r=u.bind(null,n,o,!0)}else n=i(t),a=g.bind(null,n,t),r=function(){!function(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e)}(n)};return a(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap)return;a(e=t)}else r()}}e.exports=function(e,t){(t=t||{}).singleton||"boolean"==typeof t.singleton||(t.singleton=r());var n=d(e=e||[],t);return function(e){if(e=e||[],"[object Array]"===Object.prototype.toString.call(e)){for(var a=0;a<n.length;a++){var r=l(n[a]);s[r].references--}for(var o=d(e,t),i=0;i<n.length;i++){var c=l(n[i]);0===s[c].references&&(s[c].updater(),s.splice(c,1))}n=o}}}},function(e,t){e.exports='<div class="[CLASS] fs-spread fs-odds" style="padding-top:5px;padding-bottom:5px"> [SPREAD]<br/> [ODDS] </div>'},function(e,t){e.exports='<div class="[CLASS] hide fs-total fs-odds" style="padding-top:5px;padding-bottom:5px"> [OVER_UNDER]<br/> [ODDS] </div>'},function(e,t){e.exports='<div class="[CLASS] fs-moneyline hide fs-odds" style="padding-top:15px;padding-bottom:15px"> [LINE] </div>'},function(e,t){e.exports='<tr> <td><strong>[TEAM1_VALUE]</strong></td> <td><small>[STATS_NAME]</small></td> <td><strong>[TEAM2_VALUE]</strong></td> </tr> <tr> <td colspan="3"> <div class="team1-col team-stats" style="width:[TEAM1_PER]%;background-color:[TEAM1_COLOR];height:10px"></div> <div class="team2-col team-stats" style="width:[TEAM2_PER]%;background-color:[TEAM2_COLOR];height:10px"></div> </td> </tr>'},function(e,t){e.exports='<tr> <td class="scores-table-left-col"> <div class="left"><img src="[TEAM_LOGO]" class="team-img-small"></div> <div class="left scores-name"> <strong>[TEAM_NAME]</strong><br/> <small>([WINS]-[LOSSES], [POS_WINS]-[POS_LOSSES] [POS])</small> </div> </td> <td> [P1] <div>&nbsp;</div> </td> <td> [P2] <div>&nbsp;</div> </td> <td> [P3] <div>&nbsp;</div> </td> <td> [P4] <div>&nbsp;</div> </td> <td class="scores-table-right-col"> <span style="font-size:25px;font-weight:700">[TOTAL]</span> <div>&nbsp;</div> </td> </tr>'},function(e,t){e.exports='<div class="odds-selection"> Choose Your Odds: <select name="odds-choice" id="odds-choice" class="odds-choice"> <option value="spread">Spread</option> <option value="moneyline">Moneyline</option> <option value="total">Over/Under</option> </select> </div> <table class="odds-table"> <thead> <th style="width:22%"><strong>Game</strong></th> <th style="width:13%"><strong>Draftkings</strong></th> <th style="width:13%"><strong>FanDuel</strong></th> <th style="width:13%"><strong>Sugar House</strong></th> <th style="width:13%"><strong>BetMGM</strong></th> <th style="width:13%"><strong>Unibet</strong></th> <th style="width:13%"><strong>Pointsbet</strong></th> </thead> <tbody> [ODDS_ROWS] </tbody> </table>'},function(e,t){e.exports="<tr> <td>[TEAM-BOX]</td> <td> [DraftKings_AWAY_SPREAD] [DraftKings_HOME_SPREAD] [DraftKings_OVER] [DraftKings_UNDER] [DraftKings_AWAY_LINE] [DraftKings_HOME_LINE] </td> <td> [FanDuel_AWAY_SPREAD] [FanDuel_HOME_SPREAD] [FanDuel_OVER] [FanDuel_UNDER] [FanDuel_AWAY_LINE] [FanDuel_HOME_LINE] </td> <td> [Sugarhouse_AWAY_SPREAD] [Sugarhouse_HOME_SPREAD] [Sugarhouse_OVER] [Sugarhouse_UNDER] [Sugarhouse_AWAY_LINE] [Sugarhouse_HOME_LINE] </td> <td> [BetMGM_AWAY_SPREAD] [BetMGM_HOME_SPREAD] [BetMGM_OVER] [BetMGM_UNDER] [BetMGM_AWAY_LINE] [BetMGM_HOME_LINE] </td> <td> [Unibet_AWAY_SPREAD] [Unibet_HOME_SPREAD] [Unibet_OVER] [Unibet_UNDER] [Unibet_AWAY_LINE] [Unibet_HOME_LINE] </td> <td> [PointsBet_AWAY_SPREAD] [PointsBet_HOME_SPREAD] [PointsBet_OVER] [PointsBet_UNDER] [PointsBet_AWAY_LINE] [PointsBet_HOME_LINE] </td> </tr>"},function(e,t){e.exports='<div class="team-box"> <div class="time-box"> <strong>[HOURS]</strong><br/> <small>PM EST</small> </div> <div class="vs-box"> <div class="team-logo"> <img src="[AWAY_LOGO]" class="logo"/> [AWAY_ABBR] </div> <div class="team-logo"> <img src="[HOME_LOGO]" class="logo"/> [HOME_ABBR] </div> </div> </div>'},function(e,t){e.exports='<div class="fs-player-inner-box"> <table class="player-table"> <tr> <td class="left"> <img src="[PLAYER_IMG]" class="player-img"/> </td> <td style="text-align:center"> <h4 class="player-name"> [PLAYER_NAME] <span class="player-number">[PLAYER_NUMER]</span> </h4> <div> <table class="player-stats-table"> <tr> <td><strong>Position(s)</strong><br/>[PLAYER_POS]</td> <td><strong>Weight</strong><br/>[PLAYER_WEIGHT]</td> <td><strong>Height</strong><br/>[PLAYER_HEIGHT]</td> </tr> </table> </div> </td> <td class="right"> <img src="[TEAM_LOGO]" class="player-img"/> </td> </tr> </table> <table class="player-stats-table"> <thead> <tr> <th>Year</th> <th>GP</th> <th>FG%</th> <th>3P%</th> <th>FT%</th> <th>Points</th> <th>Assists</th> <th>Steals</th> </tr> </thead> <tbody> [STATS] </tbody> </table> </div>'},function(e,t){e.exports="<tr> <td>[YEAR]</td> <td>[GP]</td> <td>[FGP]%</td> <td>[TPP]%</td> <td>[FTP]%</td> <td>[POINTS] <small>([PPG])</small></td> <td>[ASSISTS] <small>([APG])</small></td> <td>[STEALS] <small>([SPG])</small></td> </tr>"},function(e,t){e.exports='<div class="fs-matchup-inner-box"> <table class="matchup-table"> <tr> <td class="team1-col"> <img src="[TEAM1_LOGO]" class="team-img"/> <br/> <strong> [TEAM1_NAME] </strong> </td> <td> <strong>Matchup</strong> </td> <td class="team2-col"> <img src="[TEAM2_LOGO]" class="team-img"/> <br/> <strong>[TEAM2_NAME]</strong> </td> </tr> <tr> <td style="padding-top:20px">Away</td> <td style="padding-top:20px"><strong>Performance Matchup</strong></td> <td style="padding-top:20px">Home</td> </tr> [PERF_ROWS] <tr> <td style="padding-top:20px">Away</td> <td style="padding-top:20px"><strong>Per Game Matchup</strong></td> <td style="padding-top:20px">Home</td> </tr> [PER_GAME_ROWS] </table> </div>'},function(e,t){e.exports='<div class="fs-scores-inner-box"> <table class="scores-table"> <tr> <td class="scores-table-left-col"> <strong>[PERIOD]</strong> </td> <td><strong>1</strong></td> <td><strong>2</strong></td> <td><strong>3</strong></td> <td><strong>4</strong></td> <td><strong>T</strong></td> </tr> [SCORE_ROWS] </table> </div>'},function(e,t,n){var a=n(1),r=n(15);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.i,r,""]]);var o={insert:"head",singleton:!1};a(r,o);e.exports=r.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a)()(!1);r.push([e.i,".hide {\n    display: none;\n}\n.team-img  {\n    width: 100px;\n    border-radius: 20px;\n    border: 1px solid #d4d8d9;\n    padding: 5px;\n    background-color: #fff;\n}\n\n.team-img-small  {\n    width: 70px;\n    border-radius: 10px;\n    border: 1px solid #d4d8d9;\n    padding: 5px;\n    background-color: #fff;\n}\n\n\ndiv.small {\n    width: 500px;\n}\n\ndiv.medium {\n    width: 800px;\n}\n\ndiv.large {\n    width: 1000px;\n}\n\ndiv.xlarge {\n    width: 1200px;\n}\n\ndiv.right {\n    float: right;\n}\n\ndiv.left {\n    float: left;\n}",""]),t.default=r},function(e,t,n){var a=n(1),r=n(17);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.i,r,""]]);var o={insert:"head",singleton:!1};a(r,o);e.exports=r.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a)()(!1);r.push([e.i,"\n.odds-selection {\n    color: #333333;\n    font-size: 15px;\n    font-size: 0.9375rem;\n    font-family: 'Oxygen', Tahoma, Arial;\n    padding: 10px;\n    margin-bottom: 20px;\n    background-color: #ecf0f2;\n    border-radius: 3px;\n}\n\n.odds-choice {\n    font-family: 'Oxygen', Tahoma, Arial;\n    padding: 5px;\n    border-radius: 3px;\n}\n\n.odds-table {\n    color: #333333;\n    font-size: 15px;\n    font-size: 0.9375rem;\n    font-family: 'Oxygen', Tahoma, Arial;\n    /* line-height: 1.75; */\n    width: 100%;\n    border-spacing: 0;\n}\n\n.odds-table th {\n    border: 0;\n    padding: 15px 5px 15px 5px;\n}\n\n\n.odds-table td {\n    border: 0;\n    border-top: 1px solid #ecf0f2 ;\n    padding: 15px 5px 15px 5px;\n}\n\n.odds-table .team-box {\n    padding: 20px 10px 20px 10px\n}\n\n.odds-table .team-box .time-box {\n    float: left;\n    padding-right: 10px;\n    padding-top: 8px;\n}\n\n.vs-box {\n    float: left;\n}\n\n.vs-box .team-logo {\n    padding-bottom: 10px;\n}\n\n.vs-box .logo {\n    max-width: 30px;\n    vertical-align: middle;\n}\n\n.odds-table .odds-box {\n    border: 1px solid #d4d8d9;\n    background-color: #ecf0f2;\n    width: 100%;\n    line-height: 1.75;\n    text-align: center;\n    font-size: 0.75rem;\n    margin-bottom: 5px;\n    border-radius: 3px;\n}\n\n.odds-table .best {\n    background-color: #bae4f7;\n    border: 2px solid #1685b5;\n\n}",""]),t.default=r},function(e,t,n){var a=n(1),r=n(19);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.i,r,""]]);var o={insert:"head",singleton:!1};a(r,o);e.exports=r.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a)()(!1);r.push([e.i,".fs-player-box {\n    margin: auto;\n    width: 520px;\n    padding: 10px;\n}\n\n.fs-player-inner-box {\n    width: 100%;\n    border: 1px solid #ecf0f2;\n    border-radius: 3px;\n    padding: 5px;\n    background-color: #ecf0f2;\n    \n}\n.player-table {\n    color: #333333;\n    font-size: 15px;\n    font-size: 0.9375rem;\n    font-family: 'Oxygen', Tahoma, Arial;\n    /* line-height: 1.75; */\n    width: 100%;\n    border-spacing: 0;\n}\n\n.player-table td {\n    border: 0;\n    padding: 15px 5px 15px 5px;\n}\n\n.player-table .left {\n    width: 100px;\n}\n.player-table .right {\n    width: 100px;\n    text-align: right;\n}\n\n.player-img  {\n    width: 100px;\n    border-radius: 20px;\n    border: 1px solid #d4d8d9;\n    padding: 5px;\n    background-color: #fff;\n}\n\n.player-name {\n    font-size: 17px;\n    font-weight: bold;\n}\n\n.player-number {\n    font-size: 15px;\n    background-color: #333333;\n    color: #fff;\n    padding: 0px 3px 0px 3px;\n    border: 1px solid #fff;\n    border-radius: 5px;\n}\n\n.player-stats-table {\n    width: 100%;\n    padding: 0;\n    margin: 0;\n}\n\n.player-stats-table th {\n    padding: 0;\n    margin: 0;\n    font-size: 12px;\n    text-align: center;\n    font-weight: bold;\n}\n\n.player-stats-table td {\n    padding: 0;\n    margin: 0;\n    font-size: 12px;\n    text-align: center;\n}",""]),t.default=r},function(e,t,n){var a=n(1),r=n(21);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.i,r,""]]);var o={insert:"head",singleton:!1};a(r,o);e.exports=r.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a)()(!1);r.push([e.i,".fs-matchup-box {\n    width: 100%;\n    padding: 10px;\n    margin: auto;\n}\n\n.fs-matchup-inner-box {\n    border: 1px solid #ecf0f2;\n    border-radius: 3px;\n    background-color: #ecf0f2;\n    padding: 5px;\n}\n\n.matchup-table {\n    width: 100%;\n}\n\n.matchup-table td {\n    border: 0;\n    text-align: center;\n    padding-top: 8px;\n}\n\n\n\n.team-stats {\n    float: left;\n}\n",""]),t.default=r},function(e,t,n){var a=n(1),r=n(23);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.i,r,""]]);var o={insert:"head",singleton:!1};a(r,o);e.exports=r.locals||{}},function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a)()(!1);r.push([e.i,".fs-scores-box {\n    margin: auto;\n    width: 520px;\n    padding: 10px;\n}\n\n.fs-scores-inner-box {\n    width: 100%;\n    border: 1px solid #ecf0f2;\n    border-radius: 3px;\n    padding: 5px;\n    background-color: #ecf0f2;\n    \n}\n\n.scores-table {\n    width: 100%;\n    margin-bottom: 0;\n}\n\n.scores-table td {\n    border: 0;\n    text-align: center;\n    \n    vertical-align: middle;\n}\n\n.scores-table-left-col {\n    width: 50%\n}\n\n.scores-table-right-col {\n    width: 20%;\n}\n\n.team-img-small {\n    margin-right: 8px;\n}\n\n.scores-name {\n    text-align: left;\n}",""]),t.default=r},function(e,t,n){"use strict";n.r(t);const a={GAME_KEY:null,API_URL:"http://localhost:5000/"},r=e=>{const t=e.getAttribute("size");t&&(e.className=`${e.className} ${t}`);const n=e.getAttribute("float");n&&(e.className=`${e.className} ${n}`)};var o=n(7),s=n.n(o),l=n(8),d=n.n(l),i=n(9),c=n.n(i),p=n(2),u=n.n(p),g=n(3),f=n.n(g),m=n(4),_=n.n(m);const h=(e,t,n)=>{var r=new XMLHttpRequest;r.onreadystatechange=function(){if(r.readyState==XMLHttpRequest.DONE){let n=t;n||(n=a.GAME_KEY);let o=null;o=t?[JSON.parse(r.responseText).data]:JSON.parse(r.responseText).data,b(o,e,n)}};const o=new Date,s=`${o.getFullYear()}-${o.getMonth()+1}-${o.getDate()}`;let l=null;l=t?`${a.API_URL}/${n}/game/id/${t}`:`${a.API_URL}/${n}/games/date/${s}`,r.open("GET",l,!0),r.send(null)},b=(e,t,n)=>{let a=[];for(let t=0;t<e.length;t++){const r=e[t];if(n&&r.game_key!==n)continue;const o=new Date(r.start_time);let s=o.getUTCHours(),l=o.getUTCMinutes();s>12&&(s-=12),1===l.toString().length&&(l+="0");let i=d.a,p=c.a;p=p.replace("[AWAY_ABBR]",r.away_team.abbr),p=p.replace("[AWAY_LOGO]",r.away_team.logo),p=p.replace("[HOME_ABBR]",r.home_team.abbr),p=p.replace("[HOME_LOGO]",r.home_team.logo),p=p.replace("[HOURS]",`${s}:${l}`),i=i.replace("[TEAM-BOX]",p);for(let e in r.odds){let t=r.odds[e];i=E(t,e,i),i=A(t,e,i),i=x(t,e,i)}a.push(i)}t.innerHTML=s.a.replace("[ODDS_ROWS]",a.join(""));const r=document.getElementById("odds-choice");r.addEventListener("change",e=>{const t=document.getElementsByClassName("fs-odds");for(let e=0;e<t.length;e++){const n=t[e];-1===n.className.indexOf("hide")&&(n.className=n.className+" hide"),n.className.indexOf("fs-"+r.value)>-1&&(n.className=n.className.replace(" hide",""))}})},E=(e,t,n)=>{let a=u.a,r="",o="",s="",l="";e.spread&&(r=e.spread.away.spread,o=e.spread.away.odds,s=e.spread.home.spread,l=e.spread.home.odds),a=a.replace("[SPREAD]",r),a=a.replace("[ODDS]",o),a=a.replace("[CLASS]","odds-box");let d=u.a;return d=d.replace("[SPREAD]",s),d=d.replace("[ODDS]",l),d=d.replace("[CLASS]","odds-box"),n=(n=n.replace(`[${t}_AWAY_SPREAD]`,a)).replace(`[${t}_HOME_SPREAD]`,d)},A=(e,t,n)=>{let a="",r="",o="",s="";e.over_under&&(a=e.over_under.over.points,r=e.over_under.over.odds,s=e.over_under.under.points,o=e.over_under.under.odds);let l=f.a;l=l.replace("[OVER_UNDER]","o"+a),l=l.replace("[ODDS]",r),l=l.replace("[CLASS]","odds-box");let d=f.a;return d=d.replace("[OVER_UNDER]","u"+s),d=d.replace("[ODDS]",o),d=d.replace("[CLASS]","odds-box"),n=(n=n.replace(`[${t}_OVER]`,l)).replace(`[${t}_UNDER]`,d)},x=(e,t,n)=>{let a="",r="";e.money_line&&(a=e.money_line.home.odds,r=e.money_line.away.odds);let o=_.a;o=o.replace("[LINE]",r),o=o.replace("[CLASS]","odds-box");let s=_.a;return s=s.replace("[LINE]",a),s=s.replace("[CLASS]","odds-box"),n=(n=n.replace(`[${t}_AWAY_LINE]`,o)).replace(`[${t}_HOME_LINE]`,s)};var v=n(10),S=n.n(v),y=n(11),O=n.n(y);const M=(e,t,n)=>{var r=new XMLHttpRequest;r.onreadystatechange=function(){if(r.readyState==XMLHttpRequest.DONE){let n=t;n||(n=a.GAME_KEY);let o=null;o=JSON.parse(r.responseText).data,P(o,e)}};const o=new Date;o.getFullYear(),o.getMonth(),o.getDate();let s=`${a.API_URL}/${n}/player/${t}`;r.open("GET",s,!0),r.send(null)},P=(e,t)=>{let n=S.a;n=n.replace("[PLAYER_IMG]",e.bio.headshot),n=n.replace("[PLAYER_NAME]",e.bio.name),n=n.replace("[PLAYER_NUMER]",e.bio.primary_number),n=n.replace("[PLAYER_POS]",e.bio.position),n=e.bio.weight?n.replace("[PLAYER_WEIGHT]",e.bio.weight+"lbs"):n.replace("[PLAYER_WEIGHT]","n/a"),n=e.bio.height?n.replace("[PLAYER_HEIGHT]",e.bio.height):n.replace("[PLAYER_HEIGHT]","n/a"),n=n.replace("[TEAM_LOGO]",e.team.logo);const a=[];for(let t in e.seasons){let n=O.a;const r=e.seasons[t];n=n.replace("[YEAR]",t),n=n.replace("[GP]",r.games_played),n=n.replace("[FGP]",(100*r.fgpct).toFixed(0)),n=n.replace("[TPP]",(100*r.tppct).toFixed(0)),n=n.replace("[FTP]",(100*r.ftpct).toFixed(0)),n=n.replace("[POINTS]",r.points),n=n.replace("[ASSISTS]",r.assists),n=n.replace("[STEALS]",r.steals),n=n.replace("[PPG]",r.points_per_game.toFixed(2)),n=n.replace("[APG]",r.assists_per_game.toFixed(2)),n=n.replace("[SPG]",r.steals_per_game.toFixed(2)),a.push(n)}a.reverse(),n=n.replace("[STATS]",a.join("")),t.innerHTML=n};var R=n(12),T=n.n(R),L=n(5),w=n.n(L);const N=(e,t,n,r,o)=>{var s=new XMLHttpRequest;s.onreadystatechange=function(){if(s.readyState==XMLHttpRequest.DONE){let t=null;t=JSON.parse(s.responseText).data,console.log(t),D(t,e)}};let l=`${a.API_URL}/${t}/teams/${n}/${r}/${o}`;s.open("GET",l,!0),s.send(null)},D=(e,t)=>{let n=T.a;n=n.replace("[TEAM1_NAME]",e.away.details.full_name),n=n.replace("[TEAM1_LOGO]",e.away.details.logo),n=n.replace("[TEAM2_NAME]",e.home.details.full_name),n=n.replace("[TEAM2_LOGO]",e.home.details.logo);const a=[],r=[],o=[["points_per_game","Points"],["assists_per_game","Assists"],["blocks_per_game","Blocks"],["steals_per_game","Steals"],["rebs_per_game","Rebounds"],["def_rebs_per_game","Defensive Rebounds"],["fgm_per_game","Field Goals"],["tpm_per_game","3 Points"],["ftm_per_game","Free Throws"],["fouls_per_game","Fouls"]];for(let t=0;t<o.length;t++){const n=o[t],r=n[0],s=n[1];let l=w.a,d=parseInt(e.away.team_stats[r]/(e.away.team_stats[r]+e.home.team_stats[r])*100),i=100-d;l=l.replace("[TEAM1_VALUE]",e.away.team_stats[r].toFixed(0)),l=l.replace("[TEAM2_VALUE]",e.home.team_stats[r].toFixed(0)),l=l.replace("[TEAM1_PER]",d),l=l.replace("[TEAM2_PER]",i),l=l.replace("[TEAM1_COLOR]",e.away.details.color1),l=l.replace("[TEAM2_COLOR]",e.home.details.color1),l=l.replace("[STATS_NAME]",s),a.push(l)}const s=[["fgpct","Field Goal %"],["tppct","3 Point Made %"],["ftpct","Free Throw Made %"]];for(let t=0;t<s.length;t++){const n=s[t],a=n[0],o=n[1];let l=w.a,d=parseInt(e.away.team_stats[a]/(e.away.team_stats[a]+e.home.team_stats[a])*100),i=100-d;l=l.replace("[TEAM1_VALUE]",(100*e.away.team_stats[a]).toFixed(0)+"%"),l=l.replace("[TEAM2_VALUE]",(100*e.home.team_stats[a]).toFixed(0)+"%"),l=l.replace("[TEAM1_PER]",d),l=l.replace("[TEAM2_PER]",i),l=l.replace("[TEAM1_COLOR]",e.away.details.color1),l=l.replace("[TEAM2_COLOR]",e.home.details.color1),l=l.replace("[STATS_NAME]",o),r.push(l)}n=n.replace("[PER_GAME_ROWS]",a.join("")),n=n.replace("[PERF_ROWS]",r.join("")),t.innerHTML=n};var G=n(13),H=n.n(G),I=n(6),Y=n.n(I);const U=(e,t,n)=>{var r=new XMLHttpRequest;r.onreadystatechange=function(){if(r.readyState==XMLHttpRequest.DONE){let t=null;t=JSON.parse(r.responseText).data,F(t,e)}};const o=new Date;o.getFullYear(),o.getMonth(),o.getDate();let s=`${a.API_URL}/${n}/game/id/${t}`;r.open("GET",s,!0),r.send(null)},F=(e,t)=>{let n=H.a;const a=[],r=C(e,Y.a,"away"),o=C(e,Y.a,"home");a.push(r),a.push(o);let s="Not Started";s=0===e.current_period?"Not Started":"Final"===e.game_status?"Final":"Quarter "+e.current_period,n=n.replace("[PERIOD]",s),n=n.replace("[SCORE_ROWS]",a.join("")),t.innerHTML=n},C=(e,t,n)=>{t=(t=(t=(t=(t=(t=(t=t.replace("[TEAM_LOGO]",e[n+"_team"].logo)).replace("[TEAM_NAME]",e[n+"_team"].full_name)).replace("[WINS]",e[n+"_team"].standings.wins)).replace("[LOSSES]",e[n+"_team"].standings.losses)).replace("[POS_WINS]",e[n+"_team"].standings[n].wins)).replace("[POS_LOSSES]",e[n+"_team"].standings[n].losses)).replace("[POS]",n),t=e.periods[0][n+"_score"]>0?t.replace("[P1]",e.periods[0][n+"_score"]):t.replace("[P1]","-"),t=e.periods[1][n+"_score"]>0?t.replace("[P2]",e.periods[1][n+"_score"]):t.replace("[P2]","-"),t=e.periods[2][n+"_score"]>0?t.replace("[P3]",e.periods[2][n+"_score"]):t.replace("[P3]","-"),t=e.periods[3][n+"_score"]>0?t.replace("[P4]",e.periods[3][n+"_score"]):t.replace("[P4]","-");let a=0;for(let t=0;t<e.periods.length;t++)a+=e.periods[t][n+"_score"];return 0===a&&(a="-"),t=t.replace("[TOTAL]",a)};n(14),n(16),n(18),n(20),n(22);const W=()=>{(()=>{const e=document.getElementsByClassName("fs-odds-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("key"),o=n.getAttribute("league");r(n),h(n,a,o)}})(),(()=>{const e=document.getElementsByClassName("fs-player-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("key"),o=n.getAttribute("league");r(n),M(n,a,o)}})(),(()=>{const e=document.getElementsByClassName("fs-matchup-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("league"),o=n.getAttribute("team1"),s=n.getAttribute("team2"),l=n.getAttribute("season");r(n),N(n,a,l,o,s)}})(),(()=>{const e=document.getElementsByClassName("fs-scores-box");for(let t=0;t<e.length;t++){const n=e[t],a=n.getAttribute("key"),o=n.getAttribute("league");r(n),U(n,a,o)}})()};!function(e){e.fs={config:a,scan:W}}(window)}]);