package aws.example.ec2;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Collections;
import java.util.List;
import java.util.logging.Logger;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.SdkClientException;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.ec2.AmazonEC2;
import com.amazonaws.services.ec2.AmazonEC2ClientBuilder;
import com.amazonaws.services.ec2.model.*;

public class RunEC2 {

    public static void main(String[] args) throws InterruptedException {

        final String aws_access_key_id = "";
        final String aws_secret_access_key = "";
        final String pemFileName = "";

        // here using Explicitly Specifying Credentials instead of Using the Default Credential Provider Chain
        // reference: https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html
        BasicAWSCredentials awsCreds = new BasicAWSCredentials(aws_access_key_id, aws_secret_access_key);

        // Create the AmazonEC2Client object so we can call various APIs.
        String region = "us-east-2";
        AmazonEC2 ec2 = AmazonEC2ClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(awsCreds)) // here we change orignal credentials to awsCreds
                .withRegion(region)
                .build();

        // Create a new security group.
        String groupName = "group for HW01";
        String groupDesc = "hello HW01";
        String vpcId ="vpc-9e42bff5";
        try {
            CreateSecurityGroupRequest securityGroupRequest = new CreateSecurityGroupRequest()
                    .withGroupName(groupName)
                    .withDescription(groupDesc)
                    .withVpcId(vpcId);
            CreateSecurityGroupResult createSecurityGroupResult = ec2
                    .createSecurityGroup(securityGroupRequest);
            System.out.println(String.format("Security group id: %s",
                    createSecurityGroupResult.getGroupId()));
            System.out.println(String.format("Security group name: %s",
                    groupName));
        } catch (AmazonServiceException ase) {
            System.out.println(ase.getMessage());
        }

        String ipAddr = "0.0.0.0/0";

        /***
        // Get the IP of the current host, so that we can limit the Security Group
        // by default to the ip range associated with your subnet.
        try {
            InetAddress addr = InetAddress.getLocalHost();
            // Get IP Address
            ipAddr = addr.getHostAddress() + "/32";
        } catch (UnknownHostException e) {
        }
        // Create a range that you would like to populate.
        List<String> ipRanges = Collections.singletonList(ipAddr);
         ***/
        IpRange ipRange = new IpRange()
                .withCidrIp(ipAddr);

        // Open up port 22 for TCP traffic to the associated IP from above (e.g. ssh traffic).
        IpPermission ipPermission = new IpPermission()
                .withIpProtocol("tcp")
                .withFromPort(22)
                .withToPort(22)
                .withIpv4Ranges(ipRange);

        List<IpPermission> ipPermissions = Collections.singletonList(ipPermission);

        try {
            // Authorize the ports to the used.
            AuthorizeSecurityGroupIngressRequest ingressRequest = new AuthorizeSecurityGroupIngressRequest(
                    groupName, ipPermissions); // provide the IP permissions on our group
            ec2.authorizeSecurityGroupIngress(ingressRequest);
            System.out.println(String.format("Ingress port authroized: %s",
                    ipPermissions.toString()));
        } catch (AmazonServiceException ase) {
            // Ignore because this likely means the zone has already been authorized.
            System.out.println(ase.getMessage());
        }

        // our key name
        String keyName = "MyPemHW01";
        try {
            // Creates a key-pair to connect to EC2 instance
            CreateKeyPairRequest createKeyPairRequest = new CreateKeyPairRequest();
            createKeyPairRequest.withKeyName(keyName);
            CreateKeyPairResult createKeyPairResult = ec2.createKeyPair(createKeyPairRequest);
            System.out.println(String.format("Key Name: %s", keyName));

            try {
                BufferedWriter out = new BufferedWriter(new FileWriter(pemFileName));
                out.write(createKeyPairResult.getKeyPair().getKeyMaterial());
                out.close();
                System.out.println(String.format("Key pair saved: %s",pemFileName));
            } catch (IOException e) {
                Logger.getGlobal();
            }

        } catch (AmazonServiceException ase) {
            System.out.println(ase.getMessage());
        }

        try {
            // Create a request with above details to run the image
            // get the AMI name from EC2 dashboard in AWS console
            RunInstancesRequest runInstancesRequest =
                    new RunInstancesRequest();
            runInstancesRequest.withImageId("ami-00c03f7f7f2ec15c3")
                    .withInstanceType(InstanceType.T2Micro)
                    .withMinCount(1)
                    .withMaxCount(1)
                    .withKeyName(keyName)
                    .withSecurityGroups(groupName);  // provide the name of our group we created above

            // Run the EC2 instance
            RunInstancesResult result = ec2.runInstances(
                    runInstancesRequest);
            System.out.println(String.format("EC2 result: %s", result.toString()));
            System.out.println("EC2 instance successfully running!");
            System.out.println(String.format("Instance ID: %s",
                    result.getReservation().getInstances().get(0).getInstanceId()));
            System.out.println(String.format("Instance Type: %s",
                    result.getReservation().getInstances().get(0).getInstanceType()));
            System.out.println(String.format("Region: %s",
                    result.getReservation().getInstances().get(0).getPlacement().getAvailabilityZone()));

        } catch (AmazonServiceException ase) {
            System.out.println(ase.getMessage());
        }

        // get and print the public ip and DNS
        Thread.sleep(1000);
        try {
            //Create the Filter to use to find running instances
            //the created instance is probably in pending state, or wait long enough to filter a running state
            Filter filter = new Filter("instance-state-name");
            filter.withValues("pending");

            //Create a DescribeInstancesRequest
            DescribeInstancesRequest request = new DescribeInstancesRequest();
            request.withFilters(filter);

            // Find the running instances
            DescribeInstancesResult response = ec2.describeInstances(request);
            for (Reservation reservation : response.getReservations()){
                for (Instance instance : reservation.getInstances()) {
                    //Print out the results
                    System.out.println(String.format("Instance Public DNS (IPv4): %s",
                            instance.getPublicDnsName()));
                    System.out.println(String.format("Instance IPv4 Public IP: %s",
                            instance.getPublicIpAddress()));
                }
            }
        } catch (SdkClientException e) {
            e.getStackTrace();
        }

    }

}
