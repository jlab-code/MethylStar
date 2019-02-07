#!/bin/bash
(wget -O - pi.dk/3 || curl pi.dk/3 || fetch -o - pi.dk/3) | bash