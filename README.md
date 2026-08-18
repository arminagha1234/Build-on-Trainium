# Build on Trainium

A landing page for getting started with Build on Trainium.

## Getting started

> _TODO: short intro — who this is for, what you'll need (AWS account, region, access)._

## AWS 101 for Trainium (workshop)
A hands-on beginner workshop that walks through setting up AWS for Trainium end to end: IAM user, budget alerts, AWS CLI install/config, launching and connecting to a Trainium instance, running a first ML workload, and cleanup. Takes ~1.5–2 hours. Repo: [scttfrdmn/aws-101-for-trainium](https://github.com/scttfrdmn/aws-101-for-trainium).
## Increasing your vCPU limit

When you need to increase your vCPU limit, go to this link: https://pulse.aws/survey/B2D7WSLE?p=0

## How to launch a Trn2 capacity block

This is a step-by-step guide on how to launch a Trn2 capacity block: [How to Launch a Trn2 Capacity Block](https://builder.aws.com/content/38wuiaD6PtuuJdYo3QZaCxyhGvY/how-to-launch-a-trn2-capacity-block)

## Autonomous overnight optimizer

An agent that runs on a Trainium instance and keeps optimizing models
overnight, no human in the loop — cycles a seed list forever, auto-promotes
what it learns into a shared knowledge bank so subsequent models compound
those wins. Latest overnight run (native-pytorch on trn2.48xlarge):

| Model | Speedup vs eager baseline |
|-------|--------------------------:|
| Qwen3-0.6B | **13.80×** |
| Qwen3-1.7B | **11.05×** |
| Qwen3-4B   | **10.79×** |
| Qwen3-8B   |  **8.56×** |
| Qwen3-32B  |  **7.88×** |

See [`autonomous-optimizer/`](./autonomous-optimizer/) for the full leaderboard,
per-model trajectory charts, and the technical notes. Framework code:
[`trainium-optimizer`](https://github.com/arminagha1234/trainium-optimizer).

## How to invite your students

> _TODO: step-by-step guide for giving students access._
>
> 1. _TODO: Decide the access model (IAM users, IAM Identity Center, or separate accounts)._
> 2. _TODO: Create accounts / users for each student._
> 3. _TODO: Assign permissions (least-privilege policy for launching/using instances)._
> 4. _TODO: Share onboarding instructions and the vCPU survey link above._
> 5. _TODO: Set up cost controls / budgets per student or group._

## Model examples

A collection of Neuron model examples lives here: https://github.com/arminagha1234/Armin-Neuron

## Neuron agentic skills

Kiro/Claude AI agents and skills for Neuron development — NKI kernel authoring/debugging/profiling plus running models on Trainium with native PyTorch (eager + torch.compile): https://github.com/arminagha1234/neuron-agentic-development-nativept
