# -*- coding: utf-8
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import maya.cmds as cmds


# def maya_useNewAPI():
#     om 기본 버전에서는 사용안함.
#     pass


class SmoothNode(mpx.MPxDeformerNode):
    TYPE_NAME = "smooth_node"
    TYPE_ID = om.MTypeId(0x0007f7fd)

    def __init__(self):
        super(SmoothNode, self).__init__()

    def deform(self, data_block, geo_iter, matrix, multi_index):
        print("TODO: deform()")
        print("data_block", data_block)
        print("geo_iter", geo_iter)
        envelope = data_block.inputValue(self.envelope).asFloat()

        if envelope == 0:
            return

        inputAttr = mpx.cvar.MPxGeometryFilter_input
        inputGeom = mpx.cvar.MPxGeometryFilter_inputGeom
        inputHandle = data_block.outputArrayValue(inputAttr)
        inputGeomHandle = inputHandle.outputValue().child(inputGeom)
        meshMObject = inputGeomHandle.asMesh()

        meshFn = om.MFnMesh(meshMObject)
        print("meshFn", meshFn)

        vertices = om.MPointArray()
        meshFn.getPoints(vertices, om.MSpace.kObject)
        print("vertices", vertices)

        geo_iter.reset()
        while not geo_iter.isDone():
            index = geo_iter.index()
            meshFn.object()
            # self.get_dagPath_from_mfMesh(meshFn)
            # vtx_pos = self.get_connected_vertices_positions(self.get_dagPath_from_mfMesh(meshFn), index)
            # print("vtx_pos", vtx_pos)

            geo_iter.next()

    def get_connected_vertices_positions(self, meshDagPath, vertexIndex):
        meshFn = om.MFnMesh(meshDagPath)

        vertIter = om.MItMeshVertex(meshDagPath)

        vertIter.setIndex(vertexIndex)

        connectedVertices = om.MIntArray()
        vertIter.getConnectedVertices(connectedVertices)

        connectedVerticesPosition = []
        for i in range(connectedVertices.length()):
            point = om.MPoint()
            meshFn.getPoint(connectedVertices[i], point, om.MSpace.kObject)
            connectedVerticesPosition.append(point)

        return connectedVerticesPosition

    def get_dagPath_from_mfMesh(self, mFnMesh):
        meshObj = mFnMesh.object()
        selectionList = om.MSelectionList()
        selectionList.add(meshObj)
        dagPath = om.MDagPath()
        selectionList.getDagPath(0, dagPath)

        return dagPath

    @classmethod
    def creator(cls):
        return SmoothNode()

    @classmethod
    def initialize(cls):
        pass


def initializePlugin(plugin):
    vendor = "Lee Sanghun"
    version = "1.0.0"

    plugin_fn = mpx.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(SmoothNode.TYPE_NAME,
                               SmoothNode.TYPE_ID,
                               SmoothNode.creator,
                               SmoothNode.initialize,
                               mpx.MPxNode.kDeformerNode)
    except:
        om.MGlobal.displayError("Failed to register node : {}".format(SmoothNode.TYPE_NAME))

def uninitializePlugin(plugin):
    plugin_fn = mpx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(SmoothNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node : {}".format(SmoothNode.TYPE_NAME))

