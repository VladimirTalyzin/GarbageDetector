<?php

const SCRIPT_PATH = "/var/www/morfo/data/www/0v.ru/garbage/";
if (!isset($_POST["photo"]))
{
	die;
}

$photo = $_POST["photo"];

list($type, $data) = explode(';', $photo);
list(, $data)      = explode(',', $data);
$data = base64_decode($data);

$filename = date("Y-m-d_H_i_s")."_".uniqid();
$fullTemporary = SCRIPT_PATH."temporary/".$filename.".png";
file_put_contents($fullTemporary, $data);

$image = imagecreatefrompng($fullTemporary);
unlink($fullTemporary);

if (!$image)
{
	echo json_encode(["error" => "invalid_photo"]);
	die;
}

$x = imagesx($image);
$y = imagesx($image);

if ($x == 0 || $y == 0)
{
	echo json_encode(["error" => "invalid_photo_dimensions"]);
	die;
}

$ratio = $x / $y;
$needScale = false;

if ($x > 850)
{
	$x = 850;
	$y = 850 / $ratio;
	$needScale = true;
}

if ($y > 1100)
{
	$x = 1100 * $ratio;
	$y = 1100;
	$needScale = true;
}

if ($needScale)
{
	$newImage = imagecreatetruecolor($x, $y);
	imagecopyresampled($newImage, $image,0, 0, 0, 0, $x, $y, imagesx($image), imagesy($image));
	imagedestroy($image);
	$image = $newImage;
}

$fullUserFile = SCRIPT_PATH."temporary/".$filename.".jpg";
imagejpeg($image, $fullUserFile, 85);

$command = escapeshellcmd("cd ".SCRIPT_PATH);
shell_exec($command);
$command = "python3 ".SCRIPT_PATH."test_file.py ".$fullUserFile;
$command = escapeshellcmd($command);
$output = shell_exec($command);
unlink($fullUserFile);

$fullResultFile = SCRIPT_PATH."users_results/".$filename.".json";
if (file_exists($fullResultFile))
{
	echo file_get_contents($fullResultFile);
}
else
{
	echo json_encode(["error" => "error_when_response"]);
}

?>