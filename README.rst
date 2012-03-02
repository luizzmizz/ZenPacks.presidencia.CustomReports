==============================
ZenPacks.presidencia.CustomReports
==============================

.. contents::
   :depth: 3

This project is a Zenoss_ extension (ZenPack) that contains some custom 
reports. 

Requirements & Dependencies
---------------------------
This ZenPack is known to be compatible with Zenoss versions 3.2

Installation
------------
There are no dependencies for installing this ZenPack.

Normal Installation (packaged egg)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Copy it to your Zenoss server and run the following commands as the zenoss
user::

    zenpack --install <package.egg>
    zs restart

Developer Installation (link mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Copy it to your Zenoss server and run the following commands as the zenoss
user::
  
    zenpack --link --install <path.to.package.folder>
    zenoss restart

Usage
-----
Installing the ZenPack will add the following objects to your Zenoss system.

* Reports/Sistemes folder

  * Device Inventory: New report, with organizer and production state
filters, toggle columns visibility and filters by device HW/OS (but not from
installed software)

  * Checklist: New parametrizable report, based on Jane Curry's availability
report. Still has a lot of job to be done...

Screenshots
-----------
|Device Inventory Report|

.. _Zenoss: http://www.zenoss.com/

.. |Device Inventory Report| image:: https://github.com/zenoss/ZenPacks.presidencia.CustomReports/raw/master/docs/DeviceInventoryReport.png
