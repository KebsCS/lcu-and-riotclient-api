<?php
$url = $_GET['url'];
$response = file_get_contents($url);
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
echo $response;
?>
