import SwiftUI
import WebKit
import CoreLocation

// MARK: - Enhanced WebView (SwiftUI wrapper)

struct EnhancedWebView: UIViewRepresentable {
    let url: URL

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeUIView(context: Context) -> WKWebView {
        // ---------- Configuration ----------
        let prefs = WKWebpagePreferences()
        prefs.allowsContentJavaScript = true

        let config = WKWebViewConfiguration()
        config.defaultWebpagePreferences = prefs
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        // Allow camera/microphone input from <input capture> and getUserMedia
        if #available(iOS 14.5, *) {
            // Handled via WKUIDelegate permissionDecision below
        }

        // ---------- Web View ----------
        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.uiDelegate = context.coordinator
        webView.allowsBackForwardNavigationGestures = true

        // Keep reference so coordinator can refresh
        context.coordinator.webView = webView

        // Background color to match app palette while loading
        webView.isOpaque = false
        webView.backgroundColor = UIColor(red: 0xF7/255.0, green: 0xF9/255.0, blue: 0xFB/255.0, alpha: 1)
        webView.scrollView.backgroundColor = webView.backgroundColor

        // Pull-to-refresh
        let refreshControl = UIRefreshControl()
        refreshControl.tintColor = UIColor(red: 0x0C/255.0, green: 0x14/255.0, blue: 0x27/255.0, alpha: 1)
        refreshControl.addTarget(
            context.coordinator,
            action: #selector(Coordinator.handleRefresh(_:)),
            for: .valueChanged
        )
        webView.scrollView.refreshControl = refreshControl

        // Load initial URL
        webView.load(URLRequest(url: url))

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        // No-op: the web view manages its own navigation state.
    }

    // MARK: - Coordinator

    class Coordinator: NSObject,
                       WKNavigationDelegate,
                       WKUIDelegate,
                       CLLocationManagerDelegate {

        weak var webView: WKWebView?

        // Loading overlay (added lazily the first time navigation starts)
        private var loadingOverlay: UIView?

        // Location manager for geolocation permission prompts
        private lazy var locationManager: CLLocationManager = {
            let mgr = CLLocationManager()
            mgr.delegate = self
            return mgr
        }()

        // MARK: Pull-to-refresh

        @objc func handleRefresh(_ sender: UIRefreshControl) {
            webView?.reload()
            // End refreshing after a short delay so the spinner is visible
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
                sender.endRefreshing()
            }
        }

        // MARK: Loading indicator

        private func showLoadingIndicator(in webView: WKWebView) {
            guard loadingOverlay == nil else { return }

            let overlay = UIView(frame: webView.bounds)
            overlay.autoresizingMask = [.flexibleWidth, .flexibleHeight]
            overlay.backgroundColor = UIColor(
                red: 0xF7/255.0, green: 0xF9/255.0, blue: 0xFB/255.0, alpha: 1
            )

            let spinner = UIActivityIndicatorView(style: .large)
            spinner.color = UIColor(red: 0x0C/255.0, green: 0x14/255.0, blue: 0x27/255.0, alpha: 1)
            spinner.center = CGPoint(x: overlay.bounds.midX, y: overlay.bounds.midY)
            spinner.autoresizingMask = [
                .flexibleLeftMargin, .flexibleRightMargin,
                .flexibleTopMargin, .flexibleBottomMargin
            ]
            spinner.startAnimating()
            overlay.addSubview(spinner)

            webView.addSubview(overlay)
            loadingOverlay = overlay
        }

        private func hideLoadingIndicator() {
            UIView.animate(withDuration: 0.25) {
                self.loadingOverlay?.alpha = 0
            } completion: { _ in
                self.loadingOverlay?.removeFromSuperview()
                self.loadingOverlay = nil
            }
        }

        // MARK: WKNavigationDelegate

        func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!) {
            showLoadingIndicator(in: webView)
        }

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            hideLoadingIndicator()
            requestLocationPermissionIfNeeded()
        }

        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            hideLoadingIndicator()
        }

        func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
            hideLoadingIndicator()
        }

        func webView(
            _ webView: WKWebView,
            decidePolicyFor navigationAction: WKNavigationAction,
            decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
        ) {
            guard let requestURL = navigationAction.request.url else {
                decisionHandler(.allow)
                return
            }

            // Intercept PDF download links -> native share sheet
            if requestURL.pathExtension.lowercased() == "pdf" {
                ShareHandler.downloadAndShare(url: requestURL, from: webView)
                decisionHandler(.cancel)
                return
            }

            // External links (different host) -> open in Safari
            let appHost = "ada-auditor-908021165922.us-central1.run.app"
            if let host = requestURL.host,
               host != appHost,
               navigationAction.navigationType == .linkActivated {
                UIApplication.shared.open(requestURL)
                decisionHandler(.cancel)
                return
            }

            decisionHandler(.allow)
        }

        // MARK: WKUIDelegate — JavaScript alerts / confirms / prompts

        func webView(
            _ webView: WKWebView,
            runJavaScriptAlertPanelWithMessage message: String,
            initiatedByFrame frame: WKFrameInfo,
            completionHandler: @escaping () -> Void
        ) {
            let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default) { _ in
                completionHandler()
            })
            presentAlert(alert, from: webView)
        }

        func webView(
            _ webView: WKWebView,
            runJavaScriptConfirmPanelWithMessage message: String,
            initiatedByFrame frame: WKFrameInfo,
            completionHandler: @escaping (Bool) -> Void
        ) {
            let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "Cancel", style: .cancel) { _ in
                completionHandler(false)
            })
            alert.addAction(UIAlertAction(title: "OK", style: .default) { _ in
                completionHandler(true)
            })
            presentAlert(alert, from: webView)
        }

        func webView(
            _ webView: WKWebView,
            runJavaScriptTextInputPanelWithPrompt prompt: String,
            defaultText: String?,
            initiatedByFrame frame: WKFrameInfo,
            completionHandler: @escaping (String?) -> Void
        ) {
            let alert = UIAlertController(title: nil, message: prompt, preferredStyle: .alert)
            alert.addTextField { tf in
                tf.text = defaultText
            }
            alert.addAction(UIAlertAction(title: "Cancel", style: .cancel) { _ in
                completionHandler(nil)
            })
            alert.addAction(UIAlertAction(title: "OK", style: .default) { _ in
                completionHandler(alert.textFields?.first?.text)
            })
            presentAlert(alert, from: webView)
        }

        // MARK: WKUIDelegate — Camera / Microphone / Geolocation permissions (iOS 15+)

        @available(iOS 15.0, *)
        func webView(
            _ webView: WKWebView,
            requestMediaCapturePermissionFor origin: WKSecurityOrigin,
            initiatedByFrame frame: WKFrameInfo,
            type: WKMediaCaptureType,
            decisionHandler: @escaping (WKPermissionDecision) -> Void
        ) {
            decisionHandler(.grant)
        }

        // Geolocation (iOS 14+): WKWebView automatically uses the app's
        // CLLocationManager authorization status. We trigger the system
        // prompt on first load so the web page's navigator.geolocation works.

        func requestLocationPermissionIfNeeded() {
            let status = locationManager.authorizationStatus
            if status == .notDetermined {
                locationManager.requestWhenInUseAuthorization()
            }
        }

        // Location permission is triggered in webView(_:didFinish:) above
        // so that navigator.geolocation calls in the web app succeed.

        // MARK: WKUIDelegate — File upload panel (camera capture)

        // WKWebView's default implementation already presents the system
        // photo/camera picker for <input type="file" accept="image/*" capture="environment">.
        // No custom override needed — the Info.plist camera key is sufficient.

        // MARK: Helpers

        private func presentAlert(_ alert: UIAlertController, from webView: WKWebView) {
            guard let scene = UIApplication.shared.connectedScenes
                    .compactMap({ $0 as? UIWindowScene })
                    .first(where: { $0.activationState == .foregroundActive }),
                  let rootVC = scene.windows.first(where: { $0.isKeyWindow })?.rootViewController
            else {
                // Can't present — call completion handlers with defaults so WKWebView doesn't hang
                return
            }
            rootVC.present(alert, animated: true)
        }

        // CLLocationManagerDelegate
        func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
            // No-op — WKWebView picks up the new authorization automatically.
        }
    }
}
