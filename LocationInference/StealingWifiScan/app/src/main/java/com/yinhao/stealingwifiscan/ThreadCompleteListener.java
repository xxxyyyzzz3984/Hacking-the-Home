package com.yinhao.stealingwifiscan;

import java.io.IOException;

public interface ThreadCompleteListener {
    void notifyOfThreadComplete(final NotifyingThread thread);
}
