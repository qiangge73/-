package com.guodn.muxtree;

import java.util.ArrayList;
import java.util.List;

public class MuxTree {
    public int[] data = new int[3];
    public List<MuxTree> Child = new ArrayList<MuxTree>();

    @Override
    public String toString() {
        return "("+data[0]+","+data[1]+","+data[2]+")";
    }
}
