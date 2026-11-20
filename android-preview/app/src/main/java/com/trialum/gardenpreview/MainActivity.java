package com.trialum.gardenpreview;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import android.webkit.ValueCallback;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public final class MainActivity extends Activity {
    private static final String APP_HOST = "appassets.androidplatform.net";
    private static final String APP_URL =
        "https://" + APP_HOST + "/assets/index.html?preset=garden-master&view=overview";
    private static final int CREATE_JSON = 8091;
    private static final int PICK_JSON = 8092;
    private WebView webView;
    private String pendingJson;
    private ValueCallback<Uri[]> pendingFiles;

    private static boolean localUri(Uri uri) {
        return "https".equals(uri.getScheme()) &&
                APP_HOST.equalsIgnoreCase(uri.getHost()) &&
                uri.getPath() != null && uri.getPath().startsWith("/assets/");
    }
    private static WebResourceResponse blocked() {
        WebResourceResponse out = new WebResourceResponse("text/plain", "UTF-8",
                new java.io.ByteArrayInputStream(new byte[0]));
        out.setStatusCodeAndReasonPhrase(404, "Not in bundled Trialum preview");
        return out;
    }
    private String mime(String path) {
        String p = path.toLowerCase(Locale.ROOT);
        if (p.endsWith(".js") || p.endsWith(".mjs")) return "text/javascript";
        if (p.endsWith(".json") || p.endsWith(".map")) return "application/json";
        if (p.endsWith(".css")) return "text/css";
        if (p.endsWith(".html")) return "text/html";
        if (p.endsWith(".glb")) return "model/gltf-binary";
        if (p.endsWith(".png")) return "image/png";
        if (p.endsWith(".webp")) return "image/webp";
        if (p.endsWith(".svg")) return "image/svg+xml";
        if (p.endsWith(".jpg") || p.endsWith(".jpeg")) return "image/jpeg";
        if (p.endsWith(".woff2")) return "font/woff2";
        if (p.endsWith(".txt")) return "text/plain";
        if (p.endsWith(".wasm")) return "application/wasm";
        return "application/octet-stream";
    }

    private final class OfflineFiles extends WebViewClient {
        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            if (!localUri(uri)) return blocked(); // no remote fonts, ads, servers or trackers
            String path = uri.getPath().substring("/assets/".length());
            // A virtual HTTPS origin is necessary for ES modules, glTF fetch and DOM storage.
            // No user-supplied path can escape packaged assets.
            if (path.length() == 0 || path.contains("..") || path.startsWith("/") ||
                    path.contains("\\") || path.indexOf('\0') >= 0) return blocked();
            try {
                InputStream content = getAssets().open("web/" + path);
                WebResourceResponse response = new WebResourceResponse(mime(path), "UTF-8", content);
                Map<String,String> headers = new HashMap<>();
                headers.put("Access-Control-Allow-Origin", "https://" + APP_HOST);
                headers.put("X-Content-Type-Options", "nosniff");
                headers.put("Cache-Control", "public,max-age=3600");
                response.setResponseHeaders(headers);
                return response;
            } catch (Exception e) {
                return blocked();
            }
        }
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            return !localUri(request.getUrl());
        }
    }

    public final class NativeJsonBridge {
        @JavascriptInterface
        public void saveJson(String requestedName, String json) {
            if (json == null || json.length() > 8 * 1024 * 1024) return;
            String filename = requestedName == null ? "Trialum-S7-MASTER-PASS2.json"
                : requestedName.replaceAll("[^A-Za-z0-9._-]", "-");
            if (!filename.toLowerCase(Locale.ROOT).endsWith(".json")) filename += ".json";
            final String safeFilename = filename;
            runOnUiThread(() -> {
                pendingJson = json;
                try {
                    Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("application/json");
                    intent.putExtra(Intent.EXTRA_TITLE, safeFilename);
                    startActivityForResult(intent, CREATE_JSON);
                } catch (Exception e) {
                    pendingJson = null;
                    Toast.makeText(MainActivity.this, "JSON не може да се зачува", Toast.LENGTH_LONG).show();
                }
            });
        }
    }

    @Override
    @SuppressWarnings("SetJavaScriptEnabled")
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        webView.setBackgroundColor(0xFF111C20);
        webView.setWebViewClient(new OfflineFiles());
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback,
                                             FileChooserParams params) {
                if (pendingFiles != null) pendingFiles.onReceiveValue(null);
                pendingFiles = callback;
                try {
                    Intent pick = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                    pick.addCategory(Intent.CATEGORY_OPENABLE);
                    pick.setType("*/*");
                    pick.putExtra(Intent.EXTRA_MIME_TYPES,
                            new String[]{"application/json","model/gltf-binary","application/octet-stream"});
                    startActivityForResult(pick, PICK_JSON);
                } catch (Exception e) {
                    pendingFiles = null;
                    callback.onReceiveValue(null);
                }
                return true;
            }
        });
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setSupportMultipleWindows(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setDefaultTextEncodingName("UTF-8");
        webView.addJavascriptInterface(new NativeJsonBridge(), "TrialumPreviewAndroid");
        setContentView(webView);
        if (savedInstanceState == null) webView.loadUrl(APP_URL);
        else webView.restoreState(savedInstanceState);
    }

    @Override
    protected void onSaveInstanceState(Bundle state) {
        webView.saveState(state);
        super.onSaveInstanceState(state);
    }
    @Override
    protected void onActivityResult(int req, int result, Intent data) {
        super.onActivityResult(req, result, data);
        if (req == CREATE_JSON) {
            if (result == RESULT_OK && data != null && data.getData() != null &&
                    pendingJson != null) {
                try (OutputStream stream = getContentResolver().openOutputStream(data.getData())) {
                    if (stream == null) throw new java.io.IOException("No output stream");
                    stream.write(pendingJson.getBytes(StandardCharsets.UTF_8));
                    Toast.makeText(this, "Trialum JSON е зачуван!", Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    Toast.makeText(this, "Проблем при зачувување JSON", Toast.LENGTH_LONG).show();
                }
            }
            pendingJson = null;
        } else if (req == PICK_JSON) {
            if (pendingFiles != null) {
                Uri[] resultUris = result == RESULT_OK && data != null && data.getData() != null
                        ? new Uri[]{data.getData()} : null;
                pendingFiles.onReceiveValue(resultUris);
                pendingFiles = null;
            }
        }
    }
    @Override public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
    @Override protected void onPause() {
        if (webView != null) webView.onPause();
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if (webView != null) webView.onResume();
    }
    @Override protected void onDestroy() {
        if (webView != null) {
            webView.removeJavascriptInterface("TrialumPreviewAndroid");
            webView.destroy();
        }
        super.onDestroy();
    }
}
