<?php
if (!empty($_GET['q'])){
    $channel_name = $_GET['q'];

    $url = "https://functions.yandexcloud.net/d4e9p11jrv26i11egld2?integration=raw";
    $channel_name = strval($channel_name);
    $data = ["search" => $channel_name];
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
        /* Handle error */
    }
    $result = json_decode($result, true);
    // foreach($result['data']['channels']['data'] as &$user){
    //     print_r($user);
    // }
    $data = $result['data']['channels'];
}
else{
    header('Location: /');
}
?>
<head>
    <meta charset="UTF-8">
    <title>Twitch поиск канала</title>
    <link rel="stylesheet" href="index.css">
    <script src="chars.js"></script>
</head>
<body>
    <div class="topnav">
        <a class="active" onclick="GoToHomePage()">Home</a>
        <div class="search-container">
            <form method="get">
              <input type="text" placeholder="Search.." name="q">
              <button type="submit">Search</button>
            </form>
        </div>
    </div>
<div class="users">
<?php
foreach($data['data'] as &$user){
    echo '<div class="user">';
        printf('<img src=%s alt=%s class="userphoto" width="80px" height"80px">', $user['thumbnail_url'], $user['broadcaster_login']);
        printf('<p>%s</p>', $user['display_name']);
        printf('<form action="user.php" method="get">
                    <input type="hidden" name="user_id" value=%s>
                    <button type="submit" name="view">View</button>
                </form>', $user['id']);
    echo '</div>';
}
?>
</div>
</body>