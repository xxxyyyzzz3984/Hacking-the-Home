package com.yinhao.testamazonsso;

import com.amazon.identity.auth.device.AuthError;
import com.amazon.identity.auth.device.api.authorization.AuthCancellation;
import com.amazon.identity.auth.device.api.authorization.AuthorizeListener;
import com.amazon.identity.auth.device.api.authorization.AuthorizeResult;

/**
 * Created by xyh3984 on 2/16/17.
 */
public class AuthorizeListenerImpl extends AuthorizeListener {
    @Override
    public void onSuccess(final AuthorizeResult authorizeResult) {
    }

    /* There was an error during the attempt to authorize the application. */
    @Override
    public void onError(final AuthError authError) {
    }

    /* Authorization was cancelled before it could be completed. */
    @Override
    public void onCancel(final AuthCancellation authCancellation) {
    }
}
