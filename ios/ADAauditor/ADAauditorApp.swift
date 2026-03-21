import SwiftUI

@main
struct ADAauditorApp: App {
    var body: some Scene {
        WindowGroup {
            WebView(url: URL(string: "http://localhost:8000")!)
                .ignoresSafeArea()
        }
    }
}
