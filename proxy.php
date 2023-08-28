<?php
$url = $_GET['url'];
$realurl = "";
switch ($url) {
    case 'lcu/data.json':
        $realurl ='lcu/data.json';
        break;
    case 'lcu/data_info.json':
        $realurl ='lcu/data_info.json';
        break;
    case 'riotclient/data.json':
        $realurl ='riotclient/data.json';
        break;
    case 'riotclient/data_info.json':
        $realurl ='riotclient/data_info.json';
        break;
    
}
$response = file_get_contents($realurl);
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
echo $response;
?>