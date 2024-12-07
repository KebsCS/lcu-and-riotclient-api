<?php
$url = $_GET['url'] ?? null;
$allowedPaths = [
    'lcu/data.json' => 'lcu/data.json',
    'lcu/data_info.json' => 'lcu/data_info.json',
    'riotclient/data.json' => 'riotclient/data.json',
    'riotclient/data_info.json' => 'riotclient/data_info.json',
];
$realUrl = $allowedPaths[$url];
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
echo file_get_contents($realUrl);
?>