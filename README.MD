# LMBD-ONOFF-RDS

This is a simples python application to turn on and off instances based on tagging the resources. I'm using the [serverless framework](https://www.serverless.com/) to deploy two function and configure lamndas on AWS. This funcion will work for RDS Cluster, Instances and Amazon Document DB. You may think "why" documentdb but this is how AWS handle cluster.

## How To Use

Before you deploy the lamdba you have to change some configurations on `serverless.yml` as you wish

```yml
provider:
  name: aws
  runtime: python2.7
  region: us-east-1
  environment:
    RDS_REGION: us-east-1
    TAG_KEY: Environment
    TAG_VALUES: Testing,Staging
```

**region** will be the region that you lambda will be deployed **RDS_REGION** is the region that your RDS will be these values could be different. **TAG_KEY** is the Tag Key that holds the value to choose who will be turned on/off and the **TAG_VALUES** the values you want to use to indetified the resources, this last value could be a single on or a list just separately by a comma.

Below you can see the two functions one to turn ON and the secont to turn OFF based on the **CMD** variable, but the value you may want to change is the **schedule** in my case I configured to run from monday to friday to turn on at 8am and turn off at 19pm ad the resoures will be off the whole weekend of course, but you can customize this schedule.

```yml
functions:
  rds-on:
    handler: lambda_function.lambda_handler
    role: myCustRole
    events:
      - schedule: cron(0 8 ? * MON-FRI *)
    environment:
      CMD: START
  rds-off:
    handler: lambda_function.lambda_handler
    role: myCustRole
    events:
      - schedule: cron(0 19 ? * MON-FRI *)
    environment:
      CMD: STOP
```

The last piece is the IAM role that all lambda needs to access AWS resources in this case just RDS

```yml
resources:
  Resources:
    myCustRole:
      Type: AWS::IAM::Role
      Properties:
        Path: /
        RoleName: lmbd-rds-onoff-role
        AssumeRolePolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Principal:
                Service:
                  - lambda.amazonaws.com
              Action: sts:AssumeRole
        Policies:
          - PolicyName: lmbd-rds-onoff-policy
            PolicyDocument:
              Version: '2012-10-17'
              Statement:
                - Effect: Allow
                  Action:
                    - logs:CreateLogGroup
                    - logs:CreateLogStream
                    - logs:PutLogEvents
                  Resource: "*"
                - Effect: Allow
                  Action:
                    - rds:*
                  Resource: "*"
```

## Deploy

```bash
git clone https://github.com/krismorte/lmbd-onoff-rds.git

cd lmbd-onoff-rds/

sls deploy -s prd
```

dependencies
===
- nopdejs
- serverles framework
- python
- aws cli