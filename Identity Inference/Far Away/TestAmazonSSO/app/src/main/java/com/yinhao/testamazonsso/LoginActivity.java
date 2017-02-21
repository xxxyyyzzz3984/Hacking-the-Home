package com.yinhao.testamazonsso;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;

import com.amazon.identity.auth.device.AuthError;
import com.amazon.identity.auth.device.api.Listener;
import com.amazon.identity.auth.device.api.authorization.AuthCancellation;
import com.amazon.identity.auth.device.api.authorization.AuthorizationManager;
import com.amazon.identity.auth.device.api.authorization.AuthorizeListener;
import com.amazon.identity.auth.device.api.authorization.AuthorizeRequest;
import com.amazon.identity.auth.device.api.authorization.AuthorizeResult;
import com.amazon.identity.auth.device.api.authorization.ProfileScope;
import com.amazon.identity.auth.device.api.authorization.User;
import com.amazon.identity.auth.device.api.workflow.RequestContext;
import com.amazon.identity.auth.device.api.authorization.Scope;

public class LoginActivity extends AppCompatActivity {

    private RequestContext mRequestContext;
    private Button mLoginButton;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        setContentView(R.layout.activity_login);

        mRequestContext = RequestContext.create(this);

        mRequestContext.registerListener(new AuthorizeListener() {
            @Override
            public void onSuccess(AuthorizeResult authorizeResult) {
                fetchUserProfile();
            }

            @Override
            public void onError(AuthError authError) {
            }

            @Override
            public void onCancel(AuthCancellation authCancellation) {

            }
        });


        mLoginButton = (Button) findViewById(R.id.amazon_loginbtn);
        mLoginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AuthorizationManager.authorize(
                        new AuthorizeRequest.Builder(mRequestContext)
                                .addScopes(ProfileScope.profile(), ProfileScope.postalCode())
                                .build()
                );
            }
        });

        mLoginButton.performClick();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mRequestContext.onResume();
    }

    @Override
    protected void onStart() {
        super.onStart();
        Scope[] scopes = {ProfileScope.profile(), ProfileScope.postalCode()};
        AuthorizationManager.getToken(this, scopes, new Listener<AuthorizeResult, AuthError>() {
            @Override
            public void onSuccess(AuthorizeResult result) {
                if (result.getAccessToken() != null) {
                    fetchUserProfile();
                } else {
                }
            }

            @Override
            public void onError(AuthError ae) {
            }
        });
    }

    private void fetchUserProfile() {
        User.fetch(this, new Listener<User, AuthError>() {

            /* fetch completed successfully. */
            @Override
            public void onSuccess(User user) {
                final String name = user.getUserName();
                final String email = user.getUserEmail();
                final String account = user.getUserId();
                final String zipCode = user.getUserPostalCode();

                Intent intent = new Intent(getBaseContext(), DemoActivity.class);
                intent.putExtra("USER_NAME", name);
                intent.putExtra("USER_EMAIL", email);
                startActivity(intent);
            }

            /* There was an error during the attempt to get the profile. */
            @Override
            public void onError(AuthError ae) {
                System.out.println("get profile error!");
            }
        });
    }
}
