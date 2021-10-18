// SPDX-License-Identifier: MIT

pragma solidity 0.8.9;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";



contract FundMe {
    
    mapping(address => uint256) public a2v;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;
    
    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund(bool check) public payable {
        
        uint256 minUsd = 50 * 10 ** 18;
        if (check) {
            require(getRate(msg.value) >= minUsd, "You need more eth!");
        }
        a2v[msg.sender] += msg.value;
        funders.push(msg.sender);
        
    }
    
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }
    
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }
    
    function getRate(uint256 ethValue) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethInUsd = (ethPrice*ethValue)/1000000000000000000;
        return ethInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }

    
    modifier onlyOwner {
        require(msg.sender == owner, "you are not owner");
        _;
    }
    
    function withdraw() payable onlyOwner public {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++) {
            a2v[funders[funderIndex]] = 0;
        }
        funders = new address[](0);
    }
    
}
