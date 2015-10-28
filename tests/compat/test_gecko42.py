from helper import CompatTestCase
from validator.chromemanifest import ChromeManifest
from validator.compat import FX42_DEFINITION
from validator.errorbundler import ErrorBundle
from validator.testcases import content


class TestFX42Compat(CompatTestCase):
    """Test that compatibility tests for Gecko 42 are properly executed."""

    VERSION = FX42_DEFINITION

    def test_parseContentType(self):
        self.run_script_for_compat("""
            var netutil = Components
              .classes["@mozilla.org/network/util;1"]
              .getService(Components.interfaces.nsINetUtil);
            netutil.parseContentType('text/html', 'utf-8', {});
        """)
        self.assert_compat_error()

    def test_newTab_xul(self):
        """Tests that the newTab.xul overlay is not in the chrome.manifest."""

        err = ErrorBundle()
        assert content.test_newTab_xul(err, None) is None

        err.save_resource('chrome.manifest',
                          ChromeManifest('foo bar', 'chrome.manifest'))
        content.test_newTab_xul(err, None)
        assert not err.failed()

        err.save_resource(
            'chrome.manifest',
            ChromeManifest(
                ('overlay chrome://browser/content/newtab/newTab.xul '
                 'chrome://ch/content/newtab/index.xul'),
                'chrome.manifest'))
        content.test_newTab_xul(err, None)
        assert err.failed()

    def test_mozRequestAnimationFrame(self):
        self.run_script_for_compat("""
            // Don't flag comments: window.mozRequestAnimationFrame()
            window.requestAnimationFrame();
        """)
        assert not self.compat_err.errors
        assert not self.compat_err.warnings

        self.run_script_for_compat("""
            window.mozRequestAnimationFrame();
        """)
        self.assert_compat_error()
