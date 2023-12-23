<?php
if (!empty($_GET['user_id'])){
    $channel_id = $_GET['user_id'];

    $url = "https://functions.yandexcloud.net/d4e9p11jrv26i11egld2?integration=raw";
    // $channel_name = strval($channel_name);
    //channel info
    $data = ["channel_info" => $channel_id, "cur_followers" => $channel_id, "user" => $channel_id];
    $json_data = json_encode($data);
    $options = [
        'http' => [
            'header' => "Content-type: application/x-www-form-urlencoded\r\n"."User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
            'method' => 'POST',
            'content' => $json_data,
        ],
    ];
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    if ($result === false) {
        header('Location: ./');
    }
    // var_dump($result);
    $channel_info = json_decode($result, true);
    // foreach($result['data']['channels']['data'] as &$user){
    //     print_r($user);
    // }
    //$data = $result['data']['channels'];
    $info = $channel_info['data']['info']['data'][0];
    $user = $channel_info['data']['user']['data'][0];
    $cur_follows = $channel_info['data']['cur_followers'];
    
    $table_res = shell_exec("python .\\cloud.py ".$user['login']);
    $table_res = str_replace("'","\"",$table_res);
    $table = json_decode($table_res, true);
    if(is_null($table)){
        header("Location: noinfo.php");
    }
    // var_dump($table);
    $headers = array_keys($table['data'][0]);
}
else{
    header('Location: /');
}
?>
<head>
    <meta charset="UTF-8">
    <title>TwitchStat <?php echo $user['display_name'];?></title>
    <link rel="stylesheet" href="index.css">
    <script src="chars.js"></script>
</head>
<body>
    <div class="topnav">
        <a class="active" onclick="GoToHomePage()">Home</a>
        <div class="search-container">
            <form action="search.php" method="get">
              <input type="text" placeholder="Search.." name="q">
              <button type="submit">Search</button>
            </form>
        </div>
    </div>
<div id="broadcaster">
    <div id="broadcaster-img">
        <img src="<?php echo $user['profile_image_url'] ?>" alt="<?php echo $user['login'] ?>_profile">
    </div>
    <div id="broadcaster-info">
        <?php printf("<h2>%s</h2>", $user['display_name']); ?>
        <p><?php echo $user['description']; ?></p>
        <p>Текущее количество отслеживающих: <?php echo $cur_follows['total']?></p>
        <a href="https://www.twitch.tv/<?php echo $user['login'];?>" target="_blank" rel="noopener noreferrer">Перейти на Twitch канал</a>
    </div>
</div>
<div class="follow_table">
    <h3>Follow Table (за последние 12 месяцев)</h3>
    <table>
        <tr>
            <th><?php echo $headers[0]?></th>
            <th><?php echo $headers[1]?></th>
            <th><?php echo $headers[2]?></th>
            <th><?php echo $headers[3]?></th>
            <th><?php echo $headers[4]?></th>
        </tr>
        <?php
            foreach($table['data'] as &$month){
                echo "<tr>";
                foreach($month as &$stat){
                    echo "<td>".$stat."</td>";
                }
                echo "</tr>";
            }
        ?>
    </table>
</div>
</body>