<?
/****************************************************************
* PHP proxy tester - rhino@project2025.com                      *
*                                                               *
* This will perform a basic connectivity and anonymity test     *
*                                                               *
* Simply upload to a php enabled webserver and change the       *
* configurable parameters below if you so desire                *
*                                                               *
* 2005-11-11   v0.1 - Compatible with Charon v0.5.3.5           *
****************************************************************/
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head><title>Online proxy tester</title></head>
<body bgcolor="black" text="white">

<?php

// Ensure that the timeouts from fsockopen don't get reported as errors (possible, depends on the php server config)
   error_reporting(0);
// Limit the amount of proxies that can be tested at any one time
   $maximum_proxies_to_test = 5;
// Enter a password (if required) to protect the page
   $password = '';

// Actual proxyjudge part of the page
   function return_env_variables()
   {
      echo '<pre>'."\n";
      foreach ($_SERVER as $header => $value )
      {
        if ((strpos($header , 'REMOTE')!== false || strpos($header , 'HTTP')!== false || strpos($header , 'REQUEST')!== false) && ( strpos($header , 'HTTP_HOST') !== 0))
        {
        echo $header.' = '.$value."\n";
        }
      }
      echo '</pre>';
   }

// Function to go away and get the page (calls through the proxy back to itself)
   function get_judge_page($proxy)
   {
   // Depending on the server environment, this timeout setting may not be available.	
      $timeout = 15;
      $proxy_cont = '';
      list($proxy_host, $proxy_port) = explode(":", $proxy);
      $proxy_fp = fsockopen($proxy_host, $proxy_port, $errornumber, $errorstring, $timeout);
      if ($proxy_fp)
      {
         stream_set_timeout($proxy_fp, $timeout);
         fputs($proxy_fp, "GET " . $_SERVER['SCRIPT_NAME'] . "?test HTTP/1.0\r\nHost: " . $_SERVER['SERVER_NAME'] . "\r\n\r\n");
         while(!feof($proxy_fp))
         {
         	  $proxy_cont .= fread($proxy_fp,4096);
         }
         fclose($proxy_fp);
         $proxy_cont = substr($proxy_cont, strpos($proxy_cont,"\r\n\r\n")+4);
      }
      return $proxy_cont;   
   }

// Check for the control string to see if it's a valid fetch of the judge
   function check_valid_judge_response($page)
   {
      if(strlen($page) < 5)
         return false;
      return strpos($page, 'REMOTE_ADDR') !== false;
   }

// Check for the IP addresses
   function check_anonymity($page)
   {
      if(strpos($page, $_SERVER['LOCAL_ADDR']) !== false)
         return false;
      return true;
   }

// Takes and tests a proxy
// 0 - Bad proxy
// 1 - Good (non anon) proxy
// 2 - Good (anonymous) proxy
   function test_proxy($proxy)
   {
      $page = get_judge_page($proxy);
      if(!check_valid_judge_response($page))
         return 0;
      if(!check_anonymity($page))
         return 1;
      return 2;
   }

////////// Main Page ////////////

// If this is a judge request, just return the environmental variables
   if(getenv('QUERY_STRING') == "test")
   {
      return_env_variables();
   }
// Else check whether we have been passed a list of proxies to test or not
// Should really use $_POST but it's been left as $HTTP_POST_VARS for older versions of php (3.x)
   elseif( (isset($HTTP_POST_VARS['action']) && $HTTP_POST_VARS['action'] === 'fred') &&
           (isset($HTTP_POST_VARS['proxies']) && $HTTP_POST_VARS['proxies'] != '') &&
           ( (strlen($password) == 0) || (isset($HTTP_POST_VARS['password']) && $HTTP_POST_VARS['password'] === $password) ))
   {
      $proxies = explode("\n", str_replace("\r", "", $HTTP_POST_VARS['proxies']), $maximum_proxies_to_test + 1);
      
   // Set the overall time limit for the page execution to 10 mins
      set_time_limit(600);
      
   // Set up some arrays to hold the results
      $anon_proxies = array();
      $nonanon_proxies = array();
      $bad_proxies = array();
   
   // Loop through and test the proxies
      for($thisproxy = 0; $thisproxy < ($maximum_proxies_to_test > count($proxies) ? count($proxies) : $maximum_proxies_to_test); $thisproxy += 1)
      {
         echo 'Testing ' . $proxies[$thisproxy] . ' .....';
         flush();
         switch(test_proxy($proxies[$thisproxy]))
         {
            case 2:
              echo '.. Anon<br>' . "\n";
               $anon_proxies[count($anon_proxies)] = $proxies[$thisproxy];
               break;
            case 1:
              echo '.. Non anon<br>' . "\n";
               $nonanon_proxies[count($nonanon_proxies)] = $proxies[$thisproxy];
               break;
            case 0:
              echo '.. Dead<br>' . "\n";
               $bad_proxies[count($bad_proxies)] = $proxies[$thisproxy];
               break;
         }
      }
   
      echo '<pre>';
      echo '<br><b>Anonymous proxies</b>' . "\n";
      for($thisproxy = 0; $thisproxy < count($anon_proxies); $thisproxy += 1)
         echo $anon_proxies[$thisproxy] . "\n";
      echo '<br><b>Non-anonymous proxies</b>' . "\n";
      for($thisproxy = 0; $thisproxy < count($nonanon_proxies); $thisproxy += 1)
         echo $nonanon_proxies[$thisproxy] . "\n";
      echo '<br><b>Dead proxies</b>' . "\n";
      for($thisproxy = 0; $thisproxy < count($bad_proxies); $thisproxy += 1)
         echo $bad_proxies[$thisproxy] . "\n";
      echo '</pre>';
   }
// Just a blank call of the page - show the form for the user to fill in
   else
   {
      echo '<h2>Online Proxy checker</h2>' . "\n";
      echo '<h4>(http://' . $_SERVER['SERVER_NAME'] . $_SERVER['SCRIPT_NAME'] . ')</h4>' . "\n";
      echo 'Enter up to a maximum of ' . $maximum_proxies_to_test . ' prox' . ($maximum_proxies_to_test == 1 ? 'y' : 'ies') . ' to test' . "\n";
      echo '<form method="POST" action="' . $_SERVER['SCRIPT_NAME'] . '">' . "\n";
      echo '<input type="hidden" name="action" value="fred">' . "\n";
      echo '<textarea name="proxies" cols=35 rows=' . $maximum_proxies_to_test . '></textarea><br>' . "\n";
      if(strlen($password) > 0)   
         echo 'Password: <input type="password" name="password" size="15"><br>' . "\n";
      echo '<input type="submit" value="Check proxies">' . "\n";
      echo '</form>' . "\n";
   }
?>
</body>
</html>
