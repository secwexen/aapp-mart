# AI-Powered Autonomous Attack Path Prediction (AAPP)

The AI-Powered Autonomous Attack Path Prediction (AAPP) is the predictive intelligence component of AAPP-MART. It analyzes assets, identities, privileges, vulnerabilities, trust relationships, and security controls to forecast how an adversary is most likely to move through an environment.

Rather than identifying vulnerabilities in isolation, AAPP evaluates the relationships between security findings and models realistic attack progression paths.

## How It Works

The intended AAPP analysis workflow consists of several complementary stages.

### 1. Input Processing

The component receives available security information, such as asset records, vulnerability metadata, identity and permission data, and relationships defined within the supported environment model.

Input availability depends on the configured data sources and the capabilities of the installed version.

### 2. Data Normalization

Security information is organized into consistent structures so that related entities and findings can be evaluated together.

Normalization may include validating identifiers, standardizing severity information, and associating vulnerability records with relevant assets when the required data is available.

### 3. Relationship Modeling

Relevant assets and security entities can be represented as nodes, with supported relationships represented as edges in an attack graph.

The quality of this model depends on the completeness and accuracy of the supplied data. A modeled relationship should not be interpreted as proof of an actual network connection, exploitable weakness, or effective privilege unless independently verified.

### 4. Attack-Path Analysis

Where graph-based analysis is implemented, candidate paths can be examined to understand how a sequence of modeled relationships and security conditions could contribute to an adversarial objective.

The purpose is to provide context beyond isolated vulnerability records. Candidate paths remain analytical results rather than confirmation that an attacker can successfully traverse the environment.

### 5. Risk Assessment and Prioritization

Candidate paths may be evaluated using documented criteria such as the severity of contributing findings, the importance of affected assets, and the assumptions used by the analysis method.

Risk scores should be interpreted according to their documented calculation method. They should not automatically be treated as calibrated probabilities of successful exploitation.

### 6. Result Generation

Analysis results can be organized for further investigation and defensive decision-making. Depending on the implemented capabilities, these may include path descriptions, contributing findings, risk assessments, and recommended remediation actions.
