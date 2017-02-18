package com.yinhao.stealingwifiscan;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import javax.net.ssl.HttpsURLConnection;

public class ShowLocationActivity extends AppCompatActivity implements OnMapReadyCallback, ThreadCompleteListener {

    private List<String> mBssid_List;
    private List<String> mSignalLevel_List;
    private GoogleMap mMap;
    private NotifyingThread mProcessingThread;
    private String ProcessingThreadLabel = "processing_thread";
    private LatLng mCurrentLocation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_location);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        mBssid_List = new ArrayList<>();
        mSignalLevel_List = new ArrayList<>();

        // start processing data
        initilize_processingthread();
        mProcessingThread.start();
    }

    private void parse_GHDJson() {
        try {
            JSONArray All_AP_Lists = new JSONArray(MainActivity.mScanResults);
            for(int i = 0; i<All_AP_Lists.length(); i++) {
                JSONObject AP_List_JS = All_AP_Lists.getJSONObject(i);
                String AP_List_Str = AP_List_JS.getString("ap_list");

                JSONArray HotSpot_Arr = new JSONArray(AP_List_Str);
                for(int j = 0; j<HotSpot_Arr.length(); j++) {
                    JSONObject HotSpot_Js = HotSpot_Arr.getJSONObject(j);
                    mBssid_List.add(HotSpot_Js.getString("bssid"));
                    mSignalLevel_List.add(HotSpot_Js.getString("signal_level"));
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void initilize_processingthread() {
        mProcessingThread = new NotifyingThread() {
            @Override
            public void doRun() {
                // parse scan results first
                parse_GHDJson();
                String query_str = construct_query();
                String location_str = send_query(query_str);
                try {
                    JSONObject location_js = new JSONObject(location_str);
                    JSONObject latlng_js = location_js.getJSONObject("location");
                    mCurrentLocation = new LatLng(Float.parseFloat(latlng_js.getString("lat")),
                            Float.parseFloat(latlng_js.getString("lng")));
                }
                catch (JSONException e) {
                    e.printStackTrace();
                }

            }

        };

        mProcessingThread.addListener(ShowLocationActivity.this);
        mProcessingThread.label = ProcessingThreadLabel;
    }

    private String send_query(String query_str) {
        String response = "";
        try {
            URL query_url =
                    new URL("https://www.googleapis.com/geolocation/v1/geolocate?key=" +
                            getResources().getString(R.string.GOOGLE_API_KEY));
            HttpsURLConnection httpURLConnection = (HttpsURLConnection) query_url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestProperty("Content-Type", "application/json");
            httpURLConnection.setRequestMethod("POST");

            OutputStream outputStream = httpURLConnection.getOutputStream();

            BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(outputStream));
            bufferedWriter.write(query_str);
            bufferedWriter.flush();

            InputStream inputStream = new BufferedInputStream(httpURLConnection.getInputStream());
            response = IOStreamProcessing.convertInputStreamToString(inputStream);

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (ProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }

    private String construct_query() {

        JSONArray wifi_ap_arr = new JSONArray();

        for(int i = 0; i<mBssid_List.size(); i++) {
            try {
                JSONObject wifi_info_js = new JSONObject();
                wifi_info_js.put("macAddress", mBssid_List.get(i));
                wifi_info_js.put("signalStrength", Integer.parseInt(mSignalLevel_List.get(i)));
                wifi_ap_arr.put(wifi_info_js);

            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        JSONObject Query = new JSONObject();
        try {
            Query.put("considerIp", "false");
            Query.put("wifiAccessPoints", wifi_ap_arr);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return Query.toString();
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
    }

    @Override
    public void notifyOfThreadComplete(NotifyingThread thread) {
        if(thread.label.matches(ProcessingThreadLabel)) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if(mCurrentLocation != null && mMap != null) {
                        mMap.addMarker(new MarkerOptions().position(mCurrentLocation)
                                .title("Your Location"));
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(mCurrentLocation, 15));
                    }
                }
            });

        }

    }
}
