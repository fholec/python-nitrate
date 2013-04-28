#!/usr/bin/env python

import nitrate
import random
import optparse

MASTER_TP = "Master TP"
PRODUCT = nitrate.Product(name="RHEL Tests")
VERSION = nitrate.Version(product=PRODUCT, version="unspecified")
PLANTYPE = nitrate.PlanType(name="Function")
CATEGORY = nitrate.Category(category="Regression", product=PRODUCT)
CASESTATUS = nitrate.CaseStatus("CONFIRMED")
BUILD = nitrate.Build(product=PRODUCT, build="RHEL6-6.0")

TAGS = ["tag{0}".format(id) for id in range(7)]

def parse_options():
    parser = optparse.OptionParser(
            usage = "./init_tcms [--plans #] [--runs #] [--cases #]")
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

    # Create master plan (root)
    master = nitrate.TestPlan(name=MASTER_TP,
        product=PRODUCT.name, version=VERSION.name,
        type=PLANTYPE)

    for plan_count in range(0, options.plans):
        # Create Plans
        testplan = nitrate.TestPlan(name="Test Plan {0}".format(plan_count+1),
            parent=master.id, product=PRODUCT.name, version=VERSION.name,
            type=PLANTYPE)
        for case_count in range(0, options.cases):
            # Create cases
            case = nitrate.TestCase(name="Test Case {0}".format(case_count+1),
                    category=CATEGORY.name,
                    product=PRODUCT.name,
                    summary="Test Case {0}".format(case_count+1),
                    status=CASESTATUS)
            # Link with TestPlan
            nitrate.TestCase(case.id).testplans._add([testplan])
            # Add a tag
            nitrate.TestCase(case.id).tags._add(random.choice(TAGS))
        for run_count in range(0, options.runs):
            # Create runs
            run = nitrate.TestRun(name="Test Run {0}".format(run_count+1),
                    testplan=testplan.id,
                    build=BUILD.name,
                    product=PRODUCT.name, summary="Test Run",
                    version=VERSION.name)
