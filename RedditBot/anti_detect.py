import undetected_chromedriver as uc
from selenium_stealth import stealth
import os

def CreateDriver(profile):
    options = uc.ChromeOptions()

    # No need to wait till full page load
    options.page_load_strategy="eager"

    # Add proxy
    options.add_argument("--proxy-server=" + profile["proxy"])

    # Disable notifications
    options.add_argument("--disable-notifications")
    
    # Disable webgl
    options.add_argument("--disable-webgl")

    # WebRTC spoof
    current_folder = os.path.dirname(os.path.abspath(__file__))
    options.add_argument("--load-extension=" + current_folder + "\\webrtc")

    # Create driver
    driver = uc.Chrome(options=options, user_data_dir="c:\\temp\\" + profile["name"], enable_cdp_events=True)

    # For slow proxy connections
    driver.set_page_load_timeout(600)

    # Spoof driver geolocation
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", profile["coordinates"])

    # Spoof driver timezone
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", profile["timezone"])

    # Set navigator.deviceMemory
    script = """
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => """ + profile["device_memory"] + """
        });
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

    # Set navigator.platform
    script = """
        Object.defineProperty(navigator, 'platform', {
            get: () => ' """ + profile["platform"] + """'
        });
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

    # Set navigator.hardwareConcurrency
    script = """
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => ' """ + profile["hardwareConcurrency"] + """'
        });
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

    # Spoof canvas
    script = """
        const getImageData = CanvasRenderingContext2D.prototype.getImageData;
        //
        const noisify = function (canvas, context) {
            if (context) {
            const shift = {
                'r': Math.floor(""" + profile["canva_random"][0] + """ * 10) - 5,
                'g': Math.floor(""" + profile["canva_random"][1] + """ * 10) - 5,
                'b': Math.floor(""" + profile["canva_random"][2] + """ * 10) - 5,
                'a': Math.floor(""" + profile["canva_random"][3] + """ * 10) - 5
            };
            //
            const width = canvas.width;
            const height = canvas.height;
            //
            if (width && height) {
                const imageData = getImageData.apply(context, [0, 0, width, height]);
                //
                for (let i = 0; i < height; i++) {
                for (let j = 0; j < width; j++) {
                    const n = ((i * (width * 4)) + (j * 4));
                    imageData.data[n + 0] = imageData.data[n + 0] + shift.r;
                    imageData.data[n + 1] = imageData.data[n + 1] + shift.g;
                    imageData.data[n + 2] = imageData.data[n + 2] + shift.b;
                    imageData.data[n + 3] = imageData.data[n + 3] + shift.a;
                }
                }
                //
                context.putImageData(imageData, 0, 0); 
            }
            }
        };
        //
        HTMLCanvasElement.prototype.toBlob = new Proxy(HTMLCanvasElement.prototype.toBlob, {
            apply(target, self, args) {
            noisify(self, self.getContext("2d"));
            //
            return Reflect.apply(target, self, args);
            }
        });
        //
        HTMLCanvasElement.prototype.toDataURL = new Proxy(HTMLCanvasElement.prototype.toDataURL, {
            apply(target, self, args) {
            noisify(self, self.getContext("2d"));
            //
            return Reflect.apply(target, self, args);
            }
        });
        //
        CanvasRenderingContext2D.prototype.getImageData = new Proxy(CanvasRenderingContext2D.prototype.getImageData, {
            apply(target, self, args) {
            noisify(self.canvas, self);
            //
            return Reflect.apply(target, self, args);
            }
        });
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform=profile["platform"],
        webgl_vendor=profile["webgl_vendor"],
        renderer=profile["webgl_renderer"],
        fix_hairline=True,
        )

    return driver