import pkg_resources
from absl.testing import absltest
from absl.testing import parameterized

from integration_tests.dataproc_test_case import DataprocTestCase


class DatalabTestCase(DataprocTestCase):
    COMPONENT = 'datalab'
    INIT_ACTIONS = ['datalab/datalab.sh']
    PYTHON_3_INIT_ACTIONS = ['conda/bootstrap-conda.sh']

    def verify_instance(self, name):
        self.assert_instance_command(
            name, "curl {} -L {}:8080 | grep 'Google Cloud DataLab'".format(
                "--retry 10 --retry-delay 10 --retry-connrefused", name))

    @parameterized.parameters(
        ("STANDARD", ["m"]),
    )
    def test_datalab(self, configuration, machine_suffixes):
        if self.getImageOs() == 'rocky':
            self.skipTest("Not supported in Rocky Linux-based images")

        # Skip on 2.0+ version of Dataproc because it's not supported
        if self.getImageVersion() >= pkg_resources.parse_version("2.0"):
            self.skipTest("Not supported in 2.0+ images")

        init_actions = self.INIT_ACTIONS
        metadata = 'INIT_ACTIONS_REPO={}'.format(self.INIT_ACTIONS_REPO)

        self.createCluster(
            configuration,
            init_actions,
            metadata=metadata,
            scopes='cloud-platform',
            timeout_in_minutes=30)

        for machine_suffix in machine_suffixes:
            self.verify_instance("{}-{}".format(self.getClusterName(),
                                                machine_suffix))


if __name__ == '__main__':
    absltest.main()
