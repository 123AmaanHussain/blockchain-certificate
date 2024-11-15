// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Certificate {
    struct CertificateInfo {
        uint id;
        string name;
        string course;
        string issuedDate;
        bool isIssued;
    }

    mapping(address => CertificateInfo) public certificates;
    uint public certCount = 0;

    function issueCertificate(address _recipient, string memory _name, string memory _course, string memory _issuedDate) public {
        require(!certificates[_recipient].isIssued, "Certificate already issued");
        certCount++;
        certificates[_recipient] = CertificateInfo(certCount, _name, _course, _issuedDate, true);
    }

    function verifyCertificate(address _recipient) public view returns (uint, string memory, string memory, string memory, bool) {
        CertificateInfo memory cert = certificates[_recipient];
        return (cert.id, cert.name, cert.course, cert.issuedDate, cert.isIssued);
    }
}
