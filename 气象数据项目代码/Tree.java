package com.guodn.muxtree;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Tree {

    public static boolean isDone;


    public static void main(String[] args) throws Exception {
        List<MuxTree> rootNode = new ArrayList<MuxTree>();
        BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(new File("C:\\Users\\Eenie\\Desktop\\data.txt")),
                "UTF-8"));
        String line = br.readLine();
        MuxTree firstTree = new MuxTree();
        MuxTree secondTree = new MuxTree();

        int[] pos = convers(line);

        firstTree.data[0] = pos[0];
        firstTree.data[1] = pos[1];
        firstTree.data[2] = pos[2];
        secondTree.data[0] = pos[3];
        secondTree.data[1] = pos[4];
        secondTree.data[2] = pos[5];
        firstTree.Child.add(secondTree);
        rootNode.add(firstTree);

        while ((line = br.readLine()) != null) {
            pos = convers(line);
            isDone = false;
            FindNode(pos,rootNode);
            if (!isDone){
                MuxTree temp1 = new MuxTree();
                MuxTree temp2 = new MuxTree();
                temp1.data[0] = pos[0];
                temp1.data[1] = pos[1];
                temp1.data[2] = pos[2];
                temp2.data[0] = pos[3];
                temp2.data[1] = pos[4];
                temp2.data[2] = pos[5];
                temp1.Child.add(temp2);
                rootNode.add(temp1);

            }
        }

//        Print(rootNode,0);
        System.out.println("路径总数:"+rootNode.size());

        File writename = new File("C:\\Users\\Eenie\\Desktop\\path.txt");
        writename.createNewFile();
        BufferedWriter out = new BufferedWriter(new FileWriter(writename));
        OutputFile(rootNode,0,out);
        out.flush(); // 把缓存区内容压入文件
        out.close();
        /*
        String temp = br.readLine();
        temp = temp.replaceAll(" ","");
        temp = temp.replaceAll("\\[","");
        temp = temp.replaceAll("\\]","");
        System.out.println(temp.split("\\.")[1]);
        */


    }

    public static int[] convers(String temp) {
        temp = temp.replaceAll(" ", "").replaceAll("\\[", "").replaceAll("\\]", "");
        String[] sTemp = temp.split("\\.");
        int[] result = new int[6];
        for (int i = 0; i < 6; i++) result[i] = Integer.parseInt(sTemp[i]);
        return result;
    }

    public static void FindNode(int[] pos, List<MuxTree> root) {

        if (isDone)
            return;

        for (MuxTree m : root) {
            if (m.data[0] == pos[0] && m.data[1] == pos[1] && m.data[2] == pos[2]) {
                MuxTree temp = new MuxTree();
                temp.data[0] = pos[3];
                temp.data[1] = pos[4];
                temp.data[2] = pos[5];
                m.Child.add(temp);
                isDone  = true;
                return;
            }
            if (m.Child.size() > 0){
                FindNode(pos, m.Child);
            }

        }

    }

    public static void Print(List<MuxTree> tree,int level){
        for (MuxTree m : tree) {
            System.out.printf("["+level+"]");
            System.out.println(m);
            if (m.Child.size() > 0){
                Print( m.Child,level+1);
            }

        }
    }

    public static void OutputFile(List<MuxTree> tree,int level,BufferedWriter out) throws Exception{
        for (MuxTree m : tree) {
            for(int i=0;i<level-1;i++)
                out.write("│");
            if (level>1) out.write("├");
            out.write("["+level+"]");
            out.write(m.toString()+"\r\n");
            if (m.Child.size() > 0){
                OutputFile( m.Child,level+1,out);
            }

        }
    }
}
