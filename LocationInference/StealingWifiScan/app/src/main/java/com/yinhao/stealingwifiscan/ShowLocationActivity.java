package com.yinhao.stealingwifiscan;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ShowLocationActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_location);

        MainActivity.mScanResults = "[{\"ap_list\":[{\"bssid\":\"30:5a:3a:c6:e5:98\",\"frequency\":2437,\"signal_level\":-80}],\"bssid\":\"30:5a:3a:c6:e5:98\",\"signal_level\":-80,\"ssid\":\"GRACE\",\"wpa_auth\":7,\"wpa_cipher\":4},{\"ap_list\":[{\"bssid\":\"30:5a:3a:c6:e5:9c\",\"frequency\":5745,\"signal_level\":-81}],\"bssid\":\"30:5a:3a:c6:e5:9c\"," +
                "\"signal_level\":-81,\"ssid\":\"GRACE_5G\",\"wpa_auth\":7,\"wpa_cipher\":4}]";

        try {
            JSONArray All_AP_Lists = new JSONArray(MainActivity.mScanResults);
            for(int i = 0; i<All_AP_Lists.length(); i++) {
                JSONObject AP_List_JS = All_AP_Lists.getJSONObject(i);
                String AP_List_Str = AP_List_JS.getString("ap_list");

                JSONArray HotSpot_Arr = new JSONArray(AP_List_Str);
                for(int j = 0; j<HotSpot_Arr.length(); j++) {
                    JSONObject HotSpot_Js = HotSpot_Arr.getJSONObject(j);
                    String bssid = HotSpot_Js.getString("bssid");
                    String frequency = HotSpot_Js.getString("frequency");
                    String signal_level = HotSpot_Js.getString("signal_level");
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }


    }
}
