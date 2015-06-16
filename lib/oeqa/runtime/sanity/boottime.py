#[PROTEXCAT]
#\License: ALL RIGHTS RESERVED

"""System boot time"""
import os
from oeqa.oetest import oeRuntimeTest
from oeqa.utils.helper import collect_pnp_log, get_files_dir


class BootTimeTest(oeRuntimeTest):

    def _setup(self):
        (status, output) = self.target.copy_to(
            os.path.join(get_files_dir(),
                         'systemd-analyze'), "/tmp/systemd-analyze")
        self.assertEqual(
            status,
            0,
            msg="systemd-analyze could not be copied. Output: %s" %
            output)
        (status, output) = self.target.run(" ls -la /tmp/systemd-analyze")
        self.assertEqual(
            status,
            0,
            msg="Failed to find systemd-analyze command")

    def test_boot_time(self):
        self._setup()
        filename = os.path.basename(__file__)
        casename = os.path.splitext(filename)[0]
        (status, output) = self.target.run("/tmp/systemd-analyze time"
                                           " | awk -F '=' '{print $2}'")
        collect_pnp_log(casename, output)
        print "\n%s:%s\n" % (casename, output)
        self.assertEqual(status, 0, output)