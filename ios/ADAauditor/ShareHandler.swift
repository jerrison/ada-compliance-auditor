import UIKit
import WebKit

/// Handles PDF download and presentation of the native share sheet.
final class ShareHandler {

    private init() {}

    /// Downloads a PDF from the given URL, saves it locally, and presents
    /// a UIActivityViewController so the user can share via AirDrop, email,
    /// Messages, Files, etc.
    static func downloadAndShare(url: URL, from webView: WKWebView) {
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data, error == nil else {
                print("[ShareHandler] Download failed: \(error?.localizedDescription ?? "unknown error")")
                return
            }

            let fileName = url.lastPathComponent
            let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent(fileName)

            // Also persist a copy in the app's Documents directory.
            if let docsDir = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first {
                let docsURL = docsDir.appendingPathComponent(fileName)
                try? data.write(to: docsURL, options: .atomic)
            }

            do {
                try data.write(to: tempURL, options: .atomic)
            } catch {
                print("[ShareHandler] Failed to write temp file: \(error.localizedDescription)")
                return
            }

            DispatchQueue.main.async {
                guard let scene = UIApplication.shared.connectedScenes
                        .compactMap({ $0 as? UIWindowScene })
                        .first(where: { $0.activationState == .foregroundActive }),
                      let rootVC = scene.windows.first(where: { $0.isKeyWindow })?.rootViewController
                else {
                    print("[ShareHandler] Could not find root view controller.")
                    return
                }

                let activityVC = UIActivityViewController(
                    activityItems: [tempURL],
                    applicationActivities: nil
                )

                // iPad popover support: anchor at the center of the presenting view.
                if let popover = activityVC.popoverPresentationController {
                    popover.sourceView = rootVC.view
                    popover.sourceRect = CGRect(
                        x: rootVC.view.bounds.midX,
                        y: rootVC.view.bounds.midY,
                        width: 0,
                        height: 0
                    )
                    popover.permittedArrowDirections = []
                }

                rootVC.present(activityVC, animated: true)
            }
        }
        task.resume()
    }
}
