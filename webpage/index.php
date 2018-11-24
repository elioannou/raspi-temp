<!DOCTYPE html>
<html>
  <head>
    <title>Temperature in third floor </title>
    <link rel="icon" href="Temperature.ico">
    <meta charset="UTF-8">
    <meta name="description" content="Temperatures in third floor">
    <meta name="author" content="ei233">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="60">
    <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'>
    <style>
      div.container {
      width: 100%;
      border: 1px solid gray;
      font-family: Montserrat;
      }

      header, footer {
      padding: 1em;
      color: white;
      background-color: black;
      clear: left;
      text-align: center;
      }

      nav {
      float: left;
      max-width: 150px;
      margin: 0;
      padding: 1em;
      }

      nav ul {
      list-style-type: none;
      padding: 0;
      }

      nav ul a {
      text-decoration: none;
      }

      article {
      margin-left: 100px;
      border-left: 1px solid gray;
      padding: 1em;
      overflow: hidden;
      }
    </style>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
  </head>
  <body>

    <div class="container">

      <header>
	<h3>Temperature in third floor</h3>
      </header>

      <nav>
	<ul>
	  <li><a href="#">Home</a></li>
	  <li><a href="#temps_plot">48h plot</a></li>
	  <li><a href="#temps_day_comparison">Per day plot</a></li>
	</ul>
      </nav>

      <article>
      <?php
	 $file="temps_raw_data_current";
	 $file = escapeshellarg($file);
	 $line = exec('tail -n 1 '.$file);
	 $splits=explode("\t",$line);
	 $date = $splits[0];
	 $time = $splits[1];
	 $timedate = $time.' '.$date;
	 $diff = strtotime('now') - strtotime($timedate);
	 $diff_min = round((float)$diff/60);
	 $temp = round((float)$splits[2],1);
	 ?>
	<p> The temperature is <strong style="font-size: 300%; vertical-align: middle;"><?=$temp?> <sup>o</sup>C </h1></strong></p>
	<p>Last measurement was taken <?=$diff_min?> minutes ago. </p>
	<div id="temps_plot"></div>
	<h3>Plot of last 48 hours  <a href="temp_plots/temps.svg"><i class="material-icons">launch</i></a></h3>
	<img src="temp_plots/temps.svg" width=100%>
	<div id="temps_day_comparison"></div>
	<h3>Comparison with last two days <a href="temp_plots/temps_day_comparison.svg"><i class="material-icons">launch</i></a></h3>
	<img src="temp_plots/temps_day_comparison.svg" width=100%>
      </article>

      <footer>Disclaimer: No effort has been put into checking the
      accuracy of the sensor.</footer>

    </div>

  </body>
</html>
