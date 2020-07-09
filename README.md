Overview -
For my final project of CS50, I created a web application called HockeyGeek.com.
Through the use of Python, Flask, JavaScript, HTML, CSS, and an integration with the National Hockey League's API, my application allows users to view
scoreboards of all games that occur on a given day, box scores containing detailed data from each game, current rosters for every NHL team,
as well as detailed player profile pages for every player in the National Hockey League. All of the content on the following pages is generated dynamically
with the data pulled from the API, meaning that any changes in scores, rosters, player information etc. will be automatically updated within my app as well.

Homepage -
Upon loading the homepage of HockeyGeek.com, the user will be shown a scoreboard of all games that are scheduled for that day. In the event that there
are no games scheduled for that particular day (ie during the offseason), the user is shown a message stating that there are no games, and given the option
to select an alternate date through a datepicker calendar. When an alternate date is selected, the user is shown the scoreboard for the selected date.
Within the scoreboard, the user will see each team's logo, name and total goals, along with a link to the box score for that game.

Boxscore -
When a user clicks the box score link within the homepage scoreboard, they are taken to the box score page where a detailed recap of the game is shown.
Beginning at the top of the box score page, user's will find each teams logos, names, and total goals, followed by a scoring breakdown of goals per period
including any overtime periods and shoots. All of the data generated within the box score page is displayed dynamically so that if the game had 3 periods
only 3 periods are shown, and if the game had 3 periods plus 1 overtime, the scoring breakdown will then reflect 3 periods plus 1 overtime. Below the scoring
breakdown, goaltending statistics for the game are displayed.

Continuing on down the page, the next section features a game summary of each goal and penalty that occured during the game, broken down by each period of play.
For any assists awarded with each goal, those will be displayed, crediting each tean and player for their goal or assist, as well as the time that the goal
occured. Each penalty also displays the team and player penalized, length of time for the penalty, and time the penalty occured.

The final section of the box score page showcases the 3 stars awarded at the end of the game. For each of the 3 players, a player headhshot photo is show, along
with the star number awarded, and their respective team.

Select Menu Teams -
From any page within HockeyGeek.com, users will find a drop down menu in the top right corner. This menu allows users to select any NHL team, and then be directed to
a page containing that team's current roster. The roster page features each player's headshot photo, name, jersey number, position, shooting hand, height, weight,
birth date, and birth place. Within the roster, any player's photo/name can be clicked, directing the user to that player's profile page which contains additional
detailed data for that player. Each teams roster is generated dynamically so that any time a roster changes (ie player trades) those changes will be reflected the next
time the page is loaded.

Player Profile -
The player profile page shows a more detailed view of each individual player in the NHL. The top of the player profile features a recent action photo of that player,
the player's headshot, and a brief summary of the player's data including birth date, birth place, and draft information. The following section of the player profile
page displays each player's total career statistics, broken down by each season of the player's career.

League Leaders -
The final page of my application can be reached from a link in the nav menu at the top of each page. The league leaders page displays the top 5 players for 6 separate
statistical categories including goals, assists, points, plus/minue, hits, and penalty minutes. When first reaching this page, the user is automatically shown the
leaders for each of these categories for the latest season, however a dropdown menu at the top of this page allows the user to retrieve the statistical leaders for
2017 and 2018 as well. The trial version of the NHL API used for this project only allows access to this data dating back to 2017, however the full version of the API would
let users search through the entirety of the league's history.
