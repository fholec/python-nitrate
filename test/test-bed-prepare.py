#!/usr/bin/python
""" Prepare test bed - create Test Cases, Test Plans and Test Runs """

import nitrate
import random
import optparse

MASTER_TESTPLAN_NAME = "Master Test Plan"
PRODUCT = nitrate.Product(name="RHEL Tests", version="unspecified")
VERSION = nitrate.Version(product=PRODUCT, version="unspecified")
PLANTYPE = nitrate.PlanType(name="Function")
CATEGORY = nitrate.Category(category="Regression", product=PRODUCT)
CASESTATUS = nitrate.CaseStatus("CONFIRMED")
BUILD = nitrate.Build(product=PRODUCT, build="unspecified")

TAGS = [Tag(id) for id in range(3000, 3200)]
TESTERS = [nitrate.User(id) for id in range(1000, 1050)]

def parse_options():
    parser = optparse.OptionParser(
            usage = "./test-bed-prepare [--plans #] [--runs #] [--cases #]",
            description=__doc__.strip())
    parser.add_option("--plans",
            dest = "plans",
            type = "int",
            action = "store",
            default = 1,
            help = "create specified number of plans")
    parser.add_option("--runs",
            dest = "runs",
            type = "int",
            action = "store",
            default = 1,
            help = "create specified number of runs")
    parser.add_option("--cases",
            dest = "cases",
            type = "int",
            action = "store",
            default = 1,
            help = "create specified number of cases")
    return parser.parse_args()


if __name__ == "__main__":
    (options, arguments) = parse_options()

    cases = []

    for case_count in range(options.cases):
        # Create cases
        testcase = nitrate.TestCase(
                name="Test Case {0}".format(case_count+1),
                category=CATEGORY,
                product=PRODUCT,
                summary="Test Case {0}".format(case_count+1),
                status=CASESTATUS)
        # Add a tag
        testcase.tags.add([random.choice(TAGS) for counter in range(10)])
        # Add tester
        testcase.tester = random.choice(TESTERS)
        testcase.update()
        cases.append(testcase)

    # Create master plan (root)
    master = nitrate.TestPlan(name=MASTER_TESTPLAN_NAME,
        product=PRODUCT, version=VERSION,
        type=PLANTYPE)
    nitrate.info("* {0}".format(master))

    for plan_count in range(options.plans):
        # Create Plans
        testplan = nitrate.TestPlan(
                name="Test Plan {0}".format(plan_count+1),
                parent=master.id, product=PRODUCT, version=VERSION,
                type=PLANTYPE)
        # Link all test cases to plan
        testplan.testcases.add(cases)
        testplan.update()
        nitrate.info("  * {0}".format(testplan))
        for run_count in range(options.runs):
            # Create runs
            testrun = nitrate.TestRun(
                    testplan=testplan.id,
                    build=BUILD,
                    product=PRODUCT,
                    summary="Test Run {0}".format(run_count+1),
                    version=VERSION)
            nitrate.info("    * {0}".format(testrun))
