# Rubycfn, aka Binx Managed Services

 * The blurb mentions it's an abstraction layer on top of the cloud template languages of all the major cloud providers, formed as a DSL.
 * what does the cfn in RubyCFN stand for? Cloud Formation Normalization or something?
* Having it as code allows for things like linting, unit tests, etc; CloudFormation, by contrast, is json for which there are a lot less tools available (although it should be possible to create a test suite for those as well. Deep understanding of CloudFormation templates and the nuances of the AWS platform's interpretation thereof are probably necessary for that though)

 * Binx Managed Cloud seems to be bolted on top of this platform somehow. What is the site selling? A cloud template abstraction layer or Binx Managed Cloud?

 ## Binx Managed Cloud Principles & questions

 * Am I correct in assuming all of these principles are aimed towards the cloud / architecture setup, not the applications running on the platform?
 * Would "it worked on my laptop" ever be a valid argument for cloud templates? Are there e.g. simulated cloud environments for local situations? I can imagine you can fire up your docker images for example, but the cloud platforms are often a lot more than that (a major area would for example be security / users / user groups / permissions).

* in the diagram, it's shown that linting is done after unit tests; I'd put those in front (since it's often faster than running tests), or in parallel (because you can run those simultaneously).
* If it's an abstraction layer around multi cloud, why does the main ci/cd pipeline run on AWS?

## Binx Managed Cloud landing page

* The binx managed services home page is depressing as fuck - change the image to a color one please.
* A lot of fluff in the text, but what is it? Get to the point. Also reuse that diagram if that makes it clearer.
* What is the Binx Managed Cloud actually offering? In addition to the (free/open source) RubyCfn?

## RubyCFN github repository

* The summary describes it as a CloudFormation DSL, instead of a multi-cloud abstraction layer
* Commits aren't very clear; "bump version" and "add link" are not very descriptive at all. Commits need context. Prefer amend and rebase (in branches) over "fix typo" commits.
  * this is important because you want to show maturity and professionality to help instill confidence in potential customers

## Quick Start

* Probably needs a Requirements thing as well - what version of Ruby does it require? Link to Ruby installation instructions on multiple platforms.
* Should also include what knowledge is expected from the users.

## Rubycfn generated project

Would be nice to have it output a default readme as well - I assume this generated code needs to be committed into the users' repository?

Once generated, the docs could indicate better that the envs file refer to the cloud environment - me as a developer thinks these are variables passed to my application depending on which environment they run in.

Could use some links to further reading or some expected knowledge - e.g. introduction to AWS, introduction to CloudFormation templates, generic information about architecture-as-code, etc.

"A Rubycfn project lives in another universe than your application code" -> I think this sentence should be moved up (a lot) in the docs, me as a developer is currently afraid that I have to move all my code into this repository or rewrite it to ruby or what have you.

Maybe a very quick start:
* Rubycfn is and does this
* Run these commands
* Deploy on AWS with this command
* ?????
* Profit!
* Maybe make a simple .js or whatever "hello world" script that deploys to lambda and google cloud functions in parallel?

the generated example.rb stack seems to be very AWS specific, with AWS CloudFormation syntax (AWS::S3::Bucket) leaking through. I could be wrong, further reading shows more examples showing a similar syntax for different providers. I do believe that coding resources as strings is a bad idea; it looks like a leaky abstraction (it looks like CloudFormation syntax) and it looks like a stringly typed language. As a developer, I would prefer code / constant values, things that produce a compiler error when I try to do e.g. `type: AWS.S4.Bucket` instead of S3.

The generated cicd.rb has a hardcoded default github repository name - this is probably something that should be asked for during setup. It's also referenced in .env.

I don't like the hardcoded json in cicd.rb; a ruby object/struct (if there is such a thing in ruby) serialized to valid CF JSON would have my preference. Ideally it'd be agnostic, so it could be output as CF json or whatever gcp / azure require - however, this would require a proper mapping between all cloud providers, which is challenging and risks having to support the lowest common denominator. Since this is the pipeline though, and the project is advertised as having the pipeline on AWS, CF only is probably fine.

looks like the generated file uses Codebuild to create the build pipeline - would be nice to mention this somewhere.

ok so now I have a CloudFormation template and GCP template - now what? Website needs instructions on how to deploy before going into more details IMO, or the prerequisites should list having CloudFormation / GCP template experience.

Using naive cloudformation deploy command does not work, default output gives template format errors due to placeholders and the like. The instructions only help you get it set up, they don't give instructions on what you should customize after the initial generating. Maybe offer to generate one of the example stacks from the rubycfn-example repo if those work out of the box, or change the generated stacks to something that works - e.g. a simple S3 bucket or simple ec2 setup. Maybe change it to a list of example stacks (clearly marked EXAMPLE), with instructions to uncomment the relevant `include` line in the something_stack.rb file.

# OVERALL CONCLUSIONS / OPINIONS

* I feel like I have to learn Ruby in order to make this work. I'm a developer myself but never did ruby; I can imagine more ops types would be even more lost, even if the syntax inside the Concerns themselves is relatively straightforward / copy-pasteable. Ruby isn't the most readable IMO, and I'm already intimidated. (mind you I'm also intimidated by cloudformation json, too much magic string syntax for my liking). I would personally prefer JS, with javascript objects and functions and the like, or Typescript to get type checking / errors, but I'm biased in that regard.
* The Binx Managed Cloud offering is vague at best - what does it offer on top of what CloudCFN offers? Is it merely a philosophy?

## From a Studio point of view

Disclaimer: So far we / I don't actually have experience with a 'real' studio project, or even hosting something on a cloud provider beyond training / practice data.

Last year or so, our then-CTO Marc worked for a good six months on building some kind of platform for Studio, which was probably a set of GCP templates. This was never used in production, it was overkill and likely not applicable for the projects we would end up doing. The repo is still out there somewhere I'm sure.

Our goal at studio is to be live within a day. While I do believe this tool is able to do that, some advance knowledge is required. I personally believe throwing something in a manually created s3 bucket and / or deploying something on App Engine would be faster and more pragmatic than using this tool. This tool seems more like a power user tool, for people experienced with setting up larger cloud architectures and deploying multiple stacks over time - e.g. the microservices architecture at Flora Holland. Personally I don't believe we will be having such a use case at Studio - if only because I'm not a fan of microservices, and feel they add too much overhead to an already complicated problem.

I don't see what the Binx Managed Platform could do for us, in that I only see a marketing blurb on the web page, so I'm only looking at RubyCfm, the practical implementation of what the Binx Managed Platform's principles explains.

I don't think it would help our agility if server management is at a 3rd party (what it effectively would be), and I don't think it would be cost effective to have a full time cloud engineer in our team - I don't believe we're going to make software that will be that big. I don't believe we'll do (WANT to do!) big multi-cloud architectures. I believe we'll stick to single cloud, relatively simple architectures, small enough to be either clicked together in e.g. an AWS console, or in a manageable single cloudformation file.

I do see the benefit in using RubyCfm if you're a big customer like Flora Holland; they've developed their own tool, Furby, which seems to be a sequel to similar tools used at other customers - a code layer that generates CloudFormation templates, e.g. one per appllication.
